from django import template
from recruitment_cp.models import SiteContent

register = template.Library()

@register.simple_tag
def get_site_content(key):
    try:
        content = SiteContent.objects.get(page=key)
        return content
    except SiteContent.DoesNotExist:
        return None