from django import template
from language.utils import tr as utils_tr

register = template.Library()

@register.simple_tag
def tr(text: str) -> str:
    return utils_tr(text)