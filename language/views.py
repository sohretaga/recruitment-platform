from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

import json

# Create your views here.

@require_POST
def set_language(request):
    data = json.loads(request.body)
    language_code = data.get('language', settings.SITE_LANGUAGE_CODE)

    if request.user.is_authenticated:
        cache.delete(f'site_language_{request.user.username}')
        cache.set(f'site_language_{request.user.username}', language_code, timeout=31536000) # 31536000 = 1 year
        cache.delete(f'site_language_{request.session.session_key}')
        return JsonResponse({'process': 'username'})

    else:
        if not request.session.session_key:
            request.session.create()
        cache.delete(f'site_language_{request.session.session_key}')
        cache.set(f'site_language_{request.session.session_key}', language_code, timeout=604800) # 604800 = 1 week
        cache.delete(f'site_language_{request.user.username}')
        return JsonResponse({'process': 'session'})