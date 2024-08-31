from django import template
from django.db.models import F
from django.core.cache import cache
from django.conf import settings
from recruitment_cp.models import SiteContent
from language.utils import get_cache_key

register = template.Library()

@register.simple_tag
def get_site_content(key):
    try:
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)

        title_key = get_cache_key(f'title_{key}', language)
        content_key = get_cache_key(f'content_{key}', language)
        image_key = get_cache_key(f'image_{key}', '')

        title = cache.get(title_key)
        content = cache.get(content_key)
        image = cache.get(image_key)

        if not title or not content:
            site_content = SiteContent.objects.annotate(
                title=F(f'title_{language}'),
                content=F(f'content_{language}'),
            ).values('title', 'content', 'image').get(page=key)

            title = site_content['title']
            content = site_content['content']
            image = site_content.get('image', '')

            cache.set(title_key, title, None)
            cache.set(content_key, content, None)
            cache.set(image_key, image, None)

        content_dict = {
            'title': title,
            'content': content
        }

        if image:
            content_dict['image'] = image

        return content_dict

    except SiteContent.DoesNotExist:
        return ''
