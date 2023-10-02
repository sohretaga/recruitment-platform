from django import template
from recruitment_cp.models import Language

register = template.Library()

@register.simple_tag
def languages():
    langauges = Language.objects.filter(is_active=True)
    return langauges