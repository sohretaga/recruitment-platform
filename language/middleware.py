import threading
from django.core.cache import cache
from django.conf import settings

class LanguageContext:
    _storage = {}
    _lock = threading.Lock()

    @classmethod
    def set_language(cls, language_code: str):
        thread_id = threading.get_ident()
        with cls._lock:
            cls._storage[thread_id] = language_code

    @classmethod
    def get_language(cls) -> str:
        thread_id = threading.get_ident()
        with cls._lock:
            return cls._storage.get(thread_id)

    @classmethod
    def clear_language(cls):
        thread_id = threading.get_ident()
        with cls._lock:
            if thread_id in cls._storage:
                del cls._storage[thread_id]

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache_key = f"site_language_{request.user.username}"
            language_code = cache.get(cache_key, settings.DEFAULT_SITE_LANGUAGE)
        elif request.session.session_key:
            cache_key = f"site_language_{request.session.session_key}"
            language_code = cache.get(cache_key, settings.DEFAULT_SITE_LANGUAGE)
        else:
            language_code = settings.DEFAULT_SITE_LANGUAGE

        LanguageContext.set_language(language_code)
        response = self.get_response(request)
        LanguageContext.clear_language()

        return response

def get_current_user_language() -> str:
    language_code = LanguageContext.get_language()
    if not language_code:
        return settings.DEFAULT_SITE_LANGUAGE
    return language_code
