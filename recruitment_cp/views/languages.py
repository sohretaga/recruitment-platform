from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from threading import Thread

from language.models import Language, Translation
from language.utils import create_language_table
import json

#======================================================================================================
def contents(request):
    if request.user.is_superuser:
        languages = Language.objects.all()
        context = {
             'languages': languages
        }

        return render(request, 'cp/languages/contents.html', context)

    raise Http404

def contents_load(request):
    if request.user.is_superuser:
        language = request.POST.get('language')
        
        translation = Translation.objects.filter(language__code=language).values(
            'id', 'text', 'translation'
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
                del hot[index]['text']
                translation = hot[index].get('translation', None)

                if delete:
                    translation = Translation.objects.filter(pk=pk)
                    translation.delete()

                elif pk:
                    translation = Translation.objects.filter(pk=pk)
                    translation.update(**hot[index])

                index += 1

            return JsonResponse({'status': 200})
    else:
        raise Http404
    
#======================================================================================================
def languages(request):
    if request.user.is_superuser:
        return render(request, 'cp/languages/languages.html')

    raise Http404

@require_POST
def languages_load(request):
    if request.user.is_superuser:
        languages = Language.objects.all().values('id', 'code', 'name')
        json_data = json.dumps(list(languages))

        return JsonResponse(json_data, safe=False)
    else:
        raise Http404

@require_POST
def languages_save(request):
    if request.user.is_superuser:
            hot = json.loads(request.POST.get('hot'))
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                reload = hot[index].pop('reload', None)
                name = hot[index].get('name', None)
                hot[index]['code'] = hot[index]['code'].lower()

                if name:
                    if pk:
                        language = Language.objects.filter(pk=pk)
                        language.update(**hot[index])

                        if reload:
                            thread = Thread(target=create_language_table, args=(language.first(),))
                            thread.start()
                    else:
                        language = Language(**hot[index])
                        language.save()

                        thread = Thread(target=create_language_table, args=(language,))
                        thread.start()
                else:
                    language = Language.objects.filter(pk = pk)
                    language.delete()
                
                index += 1

            return JsonResponse({'status': 200})
    else:
        raise Http404