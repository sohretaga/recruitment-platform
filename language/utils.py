from django.conf import settings
from django.core.cache import cache
from language.models import Translation
import os
import re

# def create_language_table(language) -> None:
#     templates = os.path.join(settings.BASE_DIR, 'templates')

#     for root, dirs, files in os.walk(templates):
#         for file in files:

#             if file.endswith(".html"):
#                 file_path = os.path.join(root, file)

#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
#                     matches = re.findall(r'\{% tr ["\']([^"\']*)["\'] %\}', content)

#                     if matches:
#                         for text in matches:
#                             params = {
#                                 'language': language,
#                                 'text': text
#                             }

#                             translation_exists = Translation.objects.filter(**params).exists()
#                             if not translation_exists:
#                                 Translation.objects.create(**params)
#                 f.close()


def get_ignored_files():
    """ `.gitignore` dosyasındaki dosya ve dizinleri oku ve bunları bir küme olarak döndür. """
    ignored_files = set()
    gitignore_path = os.path.join(settings.BASE_DIR, '.gitignore')
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignored_files.add(line)
    return ignored_files

def is_file_ignored(file_path, ignored_files):
    """ Bir dosyanın `.gitignore` tarafından hariç tutulup tutulmadığını kontrol et. """
    relative_path = os.path.relpath(file_path, settings.BASE_DIR)
    return any(
        relative_path.startswith(ignore_path) or
        relative_path == ignore_path
        for ignore_path in ignored_files
    )

def create_language_table(language) -> None:
    # `.gitignore` dosyasını oku ve hariç tutulacak dosyaları al
    ignored_files = get_ignored_files()
    print(ignored_files)

    # Şablon klasörünü belirleme
    templates = os.path.join(settings.BASE_DIR, 'templates')
    
    # Şablon dosyalarını tarama
    for root, dirs, files in os.walk(templates):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                if not is_file_ignored(file_path, ignored_files):
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

    # Proje dizinindeki tüm Python dosyalarını tarama
    for root, dirs, files in os.walk(settings.BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if not is_file_ignored(file_path, ignored_files):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(r'tr\(["\']([^"\']*)["\']\)', content)
                        if matches:
                            for text in matches:
                                params = {
                                    'language': language,
                                    'text': text
                                }
                                translation_exists = Translation.objects.filter(**params).exists()
                                if not translation_exists:
                                    # Translation.objects.create(**params)
                                    print(params)



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