from django import template
from django.db.models import F
from django.core.cache import cache
from recruitment_cp.models import SiteContent
from language.utils import get_cache_key
from language.middleware import get_current_user_language

register = template.Library()

@register.simple_tag
def get_site_content(key):
    try:
        language = get_current_user_language()
        title = cache.get(get_cache_key(f'title_{key}', language))
        content = cache.get(get_cache_key(f'content_{key}', language))
        image = cache.get(get_cache_key(f'image_{key}', ''))

        if not title:
            title = SiteContent.translation().get(page=key).title
            cache.set(get_cache_key(f'title_{key}', language), title)

        if not content:
            content = SiteContent.translation().get(page=key).content
            cache.set(get_cache_key(f'content_{key}', language), content)

        if not image:
            image = SiteContent.translation().get(page=key).image
            cache.set(get_cache_key(f'image_{key}', ''), image)
        
        contents = {
            'title': title,
            'content': content,
            'image': image
        }
        
        return contents

    except SiteContent.DoesNotExist:
        return ''