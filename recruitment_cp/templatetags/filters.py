from django import template
from recruitment_cp.models import Language

from django import template
from django.utils.timesince import timesince
import datetime

register = template.Library()

@register.simple_tag
def languages():
    langauges = Language.objects.filter(is_active=True)
    return langauges

register = template.Library()


@register.filter
def humanize_time(value):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - value
    if diff.days >= 1:
        return value.strftime('%d %b, %Y')
    
    return f"Posted {timesince(value)} ago"
