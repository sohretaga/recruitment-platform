from django.core.cache import cache

def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications_received.filter(read=False).count()
    else:
        count = False

    return {'notification_count':count}

def selected_language(request):
    language_code = cache.get('site_language', 'en')
    return {'language_code': language_code}