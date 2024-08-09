from django.core.cache import cache
from django.conf import settings

def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications_received.filter(read=False).count()
    else:
        count = False

    return {'notification_count':count}

def selected_language(request):
    language_code = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
    return {'language_code': language_code}