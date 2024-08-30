from django import template
from django.db.models import F
from django.core.cache import cache
from django.conf import settings
from recruitment_cp.models import SiteContent
from language.utils import get_cache_key

register = template.Library()

@register.simple_tag
def get_site_content(key):
    language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
    title = cache.get(get_cache_key(f'title_{key}', language))
    content = cache.get(get_cache_key(f'content_{key}', language))
    image = cache.get(get_cache_key(f'image_{key}', ''))

    content = {
        'title': title,
        'content': content
    }

    if image:
        content['image'] = image
    
    return content