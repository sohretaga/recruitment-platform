from django.conf import settings
from django.core.cache import cache
from language.models import Translation
from language.middleware import get_current_user_language

import hashlib
import os
import re

def get_cache_key(text: str, language_code: str) -> str:
    combined_key = f'{language_code}_{text}'
    text_hash = hashlib.md5(combined_key.encode('utf-8')).hexdigest()
    cache_key = f'translation_{text_hash}'

    return cache_key

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
    language_code = get_current_user_language()
    params = {
        'language__code':language_code,
        'text': text
    }

    try:
        cache_key = get_cache_key(text, language_code)
        cached_text = cache.get(cache_key)
        if cached_text:
            return cached_text
        else:
            translation = Translation.objects.get(**params).translation
            if translation:
                cache.set(cache_key, translation, timeout=None)
                return translation

    except Translation.DoesNotExist: ...

    return text