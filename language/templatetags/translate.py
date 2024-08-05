
from django import template
from django.core.cache import cache
from language.models import Translation

register = template.Library()

@register.simple_tag
def tr(text) -> str:
    language_code = cache.get('site_language', 'en')
    params = {
        'language__code':language_code,
        'text': text
    }

    translation_exists = Translation.objects.filter(**params).exists()
    if translation_exists:
        translation = Translation.objects.get(**params).translation
        if translation:
            return translation

    return text