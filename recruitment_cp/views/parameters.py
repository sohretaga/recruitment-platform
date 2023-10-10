from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from recruitment_cp import models as cp_models
from recruitment_cp.functions import is_ajax

import json
                        
#======================================================================================================
def pm_career_type_index(request):
    return render(request, 'cp/parameters/career_type.html')

def pm_career_type_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        career_types = cp_models.ParameterCareerType.objects.filter(language=langauge).values()
        json_data = json.dumps(list(career_types))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_career_type_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    career_type = cp_models.ParameterCareerType.objects.filter(pk=id)
                    career_type.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterCareerType.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    career_type = cp_models.ParameterCareerType.objects.filter(pk=id)
                    career_type.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                career_type = cp_models.ParameterCareerType.objects.filter(pk=id)
                career_type.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError
    

#======================================================================================================
def pm_career_level_index(request):
    return render(request, 'cp/parameters/career_level.html')

def pm_career_level_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        career_levels = cp_models.ParameterCareerLevel.objects.filter(language=langauge).values()
        json_data = json.dumps(list(career_levels))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_career_level_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    career_level = cp_models.ParameterCareerLevel.objects.filter(pk=id)
                    career_level.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterCareerLevel.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    career_level = cp_models.ParameterCareerLevel.objects.filter(pk=id)
                    career_level.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                career_level = cp_models.ParameterCareerLevel.objects.filter(pk=id)
                career_level.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError
#======================================================================================================
def pm_career_type_level_index(request):
    return render(request, 'cp/parameters/career_type_level.html')

def pm_career_type_level_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        career_types_levels = cp_models.ParameterCareerTypeLevel.objects.filter(language=langauge).values()
        json_data = json.dumps(list(career_types_levels))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_career_type_level_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    career_type_level = cp_models.ParameterCareerTypeLevel.objects.filter(pk=id)
                    career_type_level.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterCareerTypeLevel.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    career_type_level = cp_models.ParameterCareerTypeLevel.objects.filter(pk=id)
                    career_type_level.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                career_type_level = cp_models.ParameterCareerTypeLevel.objects.filter(pk=id)
                career_type_level.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError

#======================================================================================================
def pm_location_index(request):
    return render(request, 'cp/parameters/location.html')

def pm_location_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        locations = cp_models.ParameterLocation.objects.filter(language=langauge).values()
        json_data = json.dumps(list(locations))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_location_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    location = cp_models.ParameterLocation.objects.filter(pk=id)
                    location.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterLocation.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    location = cp_models.ParameterLocation.objects.filter(pk=id)
                    location.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                location = cp_models.ParameterLocation.objects.filter(pk=id)
                location.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError
    
#======================================================================================================
def pm_fte_index(request):
    return render(request, 'cp/parameters/fte.html')

def pm_fte_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        fte = cp_models.ParameterFTE.objects.filter(language=langauge).values()
        json_data = json.dumps(list(fte))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_fte_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    fte = cp_models.ParameterFTE.objects.filter(pk=id)
                    fte.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterFTE.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    fte = cp_models.ParameterFTE.objects.filter(pk=id)
                    fte.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                fte = cp_models.ParameterFTE.objects.filter(pk=id)
                fte.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError

#======================================================================================================
def pm_job_catalogue_index(request):
    return render(request, 'cp/parameters/job_catalogue.html')

def pm_job_catalogue_load(request):
    if is_ajax(request) and request.POST:
        langauge = request.POST.get('language')

        job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(language=langauge).values()
        json_data = json.dumps(list(job_catalogues))

        return HttpResponse(json_data)

    else:
        raise PermissionError

def pm_job_catalogue_save(request):
    if is_ajax(request) and request.POST:
        data:str = json.loads(request.POST.get('data'))
        language:str = request.POST.get('language')
        delete_list:list[int] = eval(request.POST.get('delete_list'))
        index:int = 0

        while index < len(data):
            id:str|None = data[index].get('id', None)
            no:str|None = data[index].get('no', None)
            name:str|None = data[index].get('name', None)
            definition:str|None = data[index].get('definition', None)
            note:str|None = data[index].get('note', None)

            if no:
                if id:
                    job_catalogue = cp_models.ParameterJobCatalogue.objects.filter(pk=id)
                    job_catalogue.update(
                        no = no, name = name,
                        definition = definition, note = note)

                else:
                    cp_models.ParameterJobCatalogue.objects.create(
                        no = no, name = name, language = language,
                        definition = definition, note = note)
            else:
                if id:
                    job_catalogue = cp_models.ParameterJobCatalogue.objects.filter(pk=id)
                    job_catalogue.delete()

            index += 1
                
        # delete row with 'DEL ROW' button
        if len(delete_list) > 0:
            for id in delete_list:
                job_catalogue = cp_models.ParameterJobCatalogue.objects.filter(pk=id)
                job_catalogue.delete()

        return JsonResponse({'status':200})
    else:
        raise PermissionError