from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.core.cache import cache

from language.models import Translation
from language.utils import create_language_table, get_cache_key
import json

#======================================================================================================
def contents(request):
    if request.user.is_superuser:

        return render(request, 'cp/languages/contents.html')

    raise Http404

def contents_load(request):
    if request.user.is_superuser:
        
        translation = Translation.objects.values(
            'id', 'text', 'translation_en', 'translation_tr'
        )
        json_data = json.dumps(list(translation))

        return JsonResponse(json_data, safe=False)
    else:
        raise Http404

def contents_save(request):
    if request.user.is_superuser:
        hot = json.loads(request.POST.get('hot'))
        index = 0

        while index < len(hot):
            pk = hot[index].pop('id', None)
            delete = hot[index].pop('delete', None)
            text = hot[index].pop('text', None)

            if delete:
                translation = Translation.objects.filter(pk=pk)
                cache_key = get_cache_key(text, 'en')
                cache.delete(cache_key)

                cache_key = get_cache_key(text, 'tr')
                cache.delete(cache_key)
                translation.delete()

            elif pk:
                translation = Translation.objects.filter(pk=pk)
                translation.update(**hot[index])

                translation_text_en = hot[index].get('translation_en', None)
                if text and translation_text_en:
                    cache_key = get_cache_key(text, 'en')
                    cache.set(cache_key, translation_text_en, timeout=None)

                translation_text_tr = hot[index].get('translation_tr', None)
                if text and translation_text_tr:
                    cache_key = get_cache_key(text, 'tr')
                    cache.set(cache_key, translation_text_tr, timeout=None)

            index += 1
        return JsonResponse({'status': 200})
    else:
        raise Http404
    
def contents_generate(request):
    if request.user.is_superuser:
        create_language_table()

        return JsonResponse({'status': 200})
    else:
        raise Http404
    
#======================================================================================================