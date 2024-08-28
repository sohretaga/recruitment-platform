from django.conf import settings
from django.core.cache import cache
from language.models import Translation
import os
import re

def create_language_table(language) -> None:
    templates = os.path.join(settings.BASE_DIR, 'templates')

    for root, dirs, files in os.walk(templates):
        for file in files:

            if file.endswith(".html"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(r'\{% tr ["\']([^"\']*)["\'] %\}', content)

                    if matches:
                        for text in matches:
                            params = {
                                'language': language,
                                'text': text
                            }

                            translation_exists = Translation.objects.filter(**params).exists()
                            if not translation_exists:
                                Translation.objects.create(**params)
                f.close()

def tr(text: str) -> str:
    language_code = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
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