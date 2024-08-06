from django import template
from django.core.cache import cache
from recruitment_cp.models import SiteContent

register = template.Library()

@register.simple_tag
def get_site_content(key):
    try:
        content = SiteContent.objects.get(page=key)
        language = cache.get('site_language', 'en')
        context = {
            'image': content.image
        }

        match language:
            case 'en':
                context['title'] = content.title
                context['content'] = content.content
            case 'tr':
                context['title'] = content.title_tr
                context['content'] = content.content_tr
        
        return context

    except SiteContent.DoesNotExist:
        return ''