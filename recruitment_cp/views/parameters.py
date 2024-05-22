from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from recruitment_cp import models as cp_models
from recruitment_cp.functions import is_ajax, datetime_to_string

import json
                        
#======================================================================================================
def career_type_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/career_type.html')

    raise Http404

def career_type_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            career_types = cp_models.ParameterCareerType.objects.filter(language=language).values()
            json_data = json.dumps(list(career_types))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def career_type_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        career_types = cp_models.ParameterCareerType.objects.filter(pk=pk)
                        career_types.update(**hot[index])
                    else:
                        career_types = cp_models.ParameterCareerType(language = language, **hot[index])
                        career_types.save()
                else:
                    career_types = cp_models.ParameterCareerType.objects.filter(pk = pk)
                    career_types.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    

#======================================================================================================
def career_level_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/career_level.html')
    
    raise Http404

def career_level_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            career_levels = cp_models.ParameterCareerLevel.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(career_levels))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def career_level_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        career_level = cp_models.ParameterCareerLevel.objects.filter(pk=pk)
                        career_level.update(**hot[index])
                    else:
                        career_level = cp_models.ParameterCareerLevel(language = language, **hot[index])
                        career_level.save()
                else:
                    career_level = cp_models.ParameterCareerLevel.objects.filter(pk = pk)
                    career_level.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def career_type_level_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/career_type_level.html')
    
    raise Http404

def career_type_level_load(request):    
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            career_types_levels = cp_models.ParameterCareerTypeLevel.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(career_types_levels))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def career_type_level_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        career_types_levels = cp_models.ParameterCareerTypeLevel.objects.filter(pk=pk)
                        career_types_levels.update(**hot[index])
                    else:
                        career_types_levels = cp_models.ParameterCareerTypeLevel(language = language, **hot[index])
                        career_types_levels.save()
                else:
                    career_types_levels = cp_models.ParameterCareerTypeLevel.objects.filter(pk = pk)
                    career_types_levels.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def location_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/location.html')
    
    raise Http404

def location_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            locations = cp_models.ParameterLocation.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(locations))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def location_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        locations = cp_models.ParameterLocation.objects.filter(pk=pk)
                        locations.update(**hot[index])
                    else:
                        locations = cp_models.ParameterLocation(language = language, **hot[index])
                        locations.save()
                else:
                    locations = cp_models.ParameterLocation.objects.filter(pk = pk)
                    locations.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def country_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/country.html')
    
    raise Http404

def country_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            countries = cp_models.ParameterCountry.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(countries))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def country_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        countries = cp_models.ParameterCountry.objects.filter(pk=pk)
                        countries.update(**hot[index])
                    else:
                        countries = cp_models.ParameterCountry(language = language, **hot[index])
                        countries.save()
                else:
                    countries = cp_models.ParameterCountry.objects.filter(pk = pk)
                    countries.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================

def work_experience_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/work_experience.html')
    
    raise Http404

def work_experience_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            work_experience = cp_models.ParameterWorkExperience.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(work_experience))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def work_experience_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        work_experience = cp_models.ParameterWorkExperience.objects.filter(pk=pk)
                        work_experience.update(**hot[index])
                    else:
                        work_experience = cp_models.ParameterWorkExperience(language = language, **hot[index])
                        work_experience.save()
                else:
                    work_experience = cp_models.ParameterWorkExperience.objects.filter(pk = pk)
                    work_experience.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def fte_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/fte.html')
    
    raise Http404

def fte_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            fte = cp_models.ParameterFTE.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(fte))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def fte_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        fte = cp_models.ParameterFTE.objects.filter(pk=pk)
                        fte.update(**hot[index])
                    else:
                        fte = cp_models.ParameterFTE(language = language, **hot[index])
                        fte.save()
                else:
                    fte = cp_models.ParameterFTE.objects.filter(pk = pk)
                    fte.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def job_catalogue_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/job_catalogue.html')
    
    raise Http404

def job_catalogue_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(job_catalogues))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def job_catalogue_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(pk=pk)
                        job_catalogues.update(**hot[index])
                    else:
                        job_catalogues = cp_models.ParameterJobCatalogue(language = language, **hot[index])
                        job_catalogues.save()
                else:
                    job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(pk = pk)
                    job_catalogues.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def employee_type_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/employee_type.html')
    
    raise Http404

def employee_type_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            employee_type = cp_models.ParameterEmployeeType.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(employee_type))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def employee_type_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        employee_type = cp_models.ParameterEmployeeType.objects.filter(pk=pk)
                        employee_type.update(**hot[index])
                    else:
                        employee_type = cp_models.ParameterEmployeeType(language = language, **hot[index])
                        employee_type.save()
                else:
                    employee_type = cp_models.ParameterEmployeeType.objects.filter(pk = pk)
                    employee_type.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def vacancy_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/vacancy.html')
    
    raise Http404

def vacancy_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            vacancies = cp_models.ParameterVacancy.objects.filter(language = language)\
                .values('id', 'no', 'organization', 'career_type', 'career_level', 'location', 'fte', 'salary_minimum',
                        'salary_midpoint', 'salary_maximum', 'salary', 'job_catalogue', 'position_title', 'job_title',
                        'employment_type', 'definition', 'created_date')
            
            json_data = json.dumps(list(vacancies), default=datetime_to_string)

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def vacancy_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                position_title = hot[index].get('position_title', None)

                if position_title:
                    if pk:
                        vacancies = cp_models.ParameterVacancy.objects.filter(pk=pk)
                        vacancies.update(**hot[index])
                    else:
                        vacancies = cp_models.ParameterVacancy(language = language, **hot[index])
                        vacancies.save()
                else:
                    vacancies = cp_models.ParameterVacancy.objects.filter(pk = pk)
                    vacancies.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404