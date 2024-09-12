import threading
from django.utils import translation
from django.core.cache import cache
from django.conf import settings

_user_language = threading.local()

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache_key = f"site_language_{request.user.username}"
            language_code = cache.get(cache_key, settings.DEFUALT_SITE_LANGUAGE)
            _user_language.value = language_code

        elif request.session.session_key:
            cache_key = f"site_language_{request.session.session_key}"
            language_code = cache.get(cache_key, settings.DEFUALT_SITE_LANGUAGE)
            _user_language.value = language_code

        else:
            _user_language.value = settings.DEFUALT_SITE_LANGUAGE
        
        response = self.get_response(request)
        return response

def get_current_user_language() -> str:
    return getattr(_user_language, 'value', settings.DEFUALT_SITE_LANGUAGE)