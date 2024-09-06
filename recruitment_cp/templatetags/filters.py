from django import template
from django import template

from main.utils import humanize_time as main_humanize_time
from recruitment_cp.models import Language
from language.utils import tr

register = template.Library()

@register.simple_tag
def languages():
    langauges = Language.objects.filter(is_active=True)
    return langauges

@register.filter
def humanize_time(value):
    return main_humanize_time(value)

@register.filter
def humanize_date(value) -> str:
    if value:
        translated_month_name = tr(value.strftime('%B'))
        return f'{value.day} {translated_month_name}, {value.year}'