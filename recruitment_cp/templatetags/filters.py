from django import template
from django import template

from main.utils import humanize_time as main_humanize_time
from recruitment_cp.models import Language

register = template.Library()

@register.simple_tag
def languages():
    langauges = Language.objects.filter(is_active=True)
    return langauges

@register.filter
def humanize_time(value):
    return main_humanize_time(value)