from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.db.models import F

from recruitment_cp import models as cp_models
from blog.models import Category as BlogCategory
from job.models import Vacancy
from user.models import Candidate, Employer
from recruitment_cp.utils import is_ajax, datetime_to_string

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
            
            career_types = cp_models.ParameterCareerType.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
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
            
            job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(language=language)\
                .values('id', 'no', 'name', 'definition', 'note', 'job_family', 'job_sub_family', 'career_type',
                        'career_level', 'typical_education', 'relevant_experience', 'job_code')
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
            offset = int(request.POST.get('offset', 0))
            limit = int(request.POST.get('limit', 1000))
            
            vacancies = Vacancy.objects.filter(language = language).select_related(
                'employer', 'career_type', 'career_level', 'location', 'fte', 'job_title', 'employment_type', 'work_experience', 'work_preference', 'department'
                ).annotate(company_name=F('employer__user__first_name'),
                           career_type_name=F('career_type__name'),
                           career_level_name=F('career_level__name'),
                           location_name=F('location__name'),
                           fte_name=F('fte__name'),
                           job_title_name=F('job_title__name'),
                           employment_type_name=F('employment_type__name'),
                           work_experience_name=F('work_experience__name'),
                           work_preference_name=F('work_preference__name'),
                           department_name=F('department__name')
                ).values()[offset:offset+limit]
            
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

                # If they are not deleted, ForeignKey gives an error
                if hot[index]['employer__user__first_name']:
                    del hot[index]['employer__user__first_name']

                if position_title:
                    if pk:
                        vacancies = Vacancy.objects.filter(pk=pk)
                        vacancies.update(**hot[index])
                    else:
                        vacancies = Vacancy(language = language, **hot[index])
                        vacancies.employer = request.user.employer
                        vacancies.save()
                else:
                    vacancies = Vacancy.objects.filter(pk = pk)
                    vacancies.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def blog_category_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/blog_category.html')
    
    raise Http404

def blog_category_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            
            blog_category = BlogCategory.objects.all().values()
            
            json_data = json.dumps(list(blog_category))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def blog_category_save(request):
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
                        blog_category = BlogCategory.objects.filter(pk=pk)
                        blog_category.update(**hot[index])
                    else:
                        blog_category = BlogCategory(**hot[index])
                        blog_category.save()
                else:
                    blog_category = BlogCategory.objects.filter(pk = pk)
                    blog_category.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def company_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/companies.html')
    
    raise Http404

def company_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            
            company = Employer.objects.all().values(
                'id', 'user__email', 'user__profile_photo', 'no', 'user__first_name', 'sector', 'organization_type', 'organization_ownership',
                'number_of_employees', 'second_email', 'other_email', 'note', 'slider'
            ).order_by('user__first_name')
            
            json_data = json.dumps(list(company), default=datetime_to_string)

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def company_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('user__first_name', None)

                # If they are not deleted, ForeignKey gives an error
                del hot[index]['user__email']
                del hot[index]['user__profile_photo']
                del hot[index]['user__first_name']

                # if name:
                if pk:
                    company = Employer.objects.filter(pk=pk)
                    company.update(**hot[index])
                else:
                    company = Employer(**hot[index])
                    company.save()
                # else:
                #     company = Employer.objects.filter(pk = pk)
                #     company.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def candidate_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/candidates.html')
    
    raise Http404

def candidate_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            
            candidate = Candidate.objects.all().values(
                'user__first_name', 'user__last_name', 'user__email', 'user__username'
            )
            
            json_data = json.dumps(list(candidate))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def candidate_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name:
                    if pk:
                        candidate = Candidate.objects.filter(pk=pk)
                        candidate.update(**hot[index])
                    else:
                        candidate = Candidate(**hot[index])
                        candidate.save()
                else:
                    candidate = Candidate.objects.filter(pk = pk)
                    candidate.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def sector_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/sector.html')
    
    raise Http404

def sector_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            sector = cp_models.ParameterSector.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(sector))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def sector_save(request):
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
                        sector = cp_models.ParameterSector.objects.filter(pk=pk)
                        sector.update(**hot[index])
                    else:
                        sector = cp_models.ParameterSector(language = language, **hot[index])
                        sector.save()
                else:
                    sector = cp_models.ParameterSector.objects.filter(pk = pk)
                    sector.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def organization_type_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/organization_type.html')
    
    raise Http404

def organization_type_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            organization_type = cp_models.ParameterOrganizationType.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(organization_type))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def organization_type_save(request):
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
                        organization_type = cp_models.ParameterOrganizationType.objects.filter(pk=pk)
                        organization_type.update(**hot[index])
                    else:
                        organization_type = cp_models.ParameterOrganizationType(language = language, **hot[index])
                        organization_type.save()
                else:
                    organization_type = cp_models.ParameterOrganizationType.objects.filter(pk = pk)
                    organization_type.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def organization_ownership_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/organization_ownership.html')
    
    raise Http404

def organization_ownership_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            organization_ownership = cp_models.ParameterOrganizationOwnership.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(organization_ownership))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def organization_ownership_save(request):
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
                        organization_ownership = cp_models.ParameterOrganizationOwnership.objects.filter(pk=pk)
                        organization_ownership.update(**hot[index])
                    else:
                        organization_ownership = cp_models.ParameterOrganizationOwnership(language = language, **hot[index])
                        organization_ownership.save()
                else:
                    organization_ownership = cp_models.ParameterOrganizationOwnership.objects.filter(pk = pk)
                    organization_ownership.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def number_of_employees_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/number_of_employees.html')
    
    raise Http404

def number_of_employees_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            number_of_employees = cp_models.ParameterNumberOfEmployee.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(number_of_employees))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def number_of_employees_save(request):
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
                        number_of_employees = cp_models.ParameterNumberOfEmployee.objects.filter(pk=pk)
                        number_of_employees.update(**hot[index])
                    else:
                        number_of_employees = cp_models.ParameterNumberOfEmployee(language = language, **hot[index])
                        number_of_employees.save()
                else:
                    number_of_employees = cp_models.ParameterNumberOfEmployee.objects.filter(pk = pk)
                    number_of_employees.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def department_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/department.html')
    
    raise Http404

def department_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            department = cp_models.ParameterDepartment.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(department))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def department_save(request):
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
                        department = cp_models.ParameterDepartment.objects.filter(pk=pk)
                        department.update(**hot[index])
                    else:
                        department = cp_models.ParameterDepartment(language=language, **hot[index])
                        department.save()
                else:
                    department = cp_models.ParameterDepartment.objects.filter(pk = pk)
                    department.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def work_preference_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/work_preference.html')
    
    raise Http404

def work_preference_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            work_preference = cp_models.ParameterWorkPreference.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(work_preference))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def work_preference_save(request):
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
                        work_preference = cp_models.ParameterWorkPreference.objects.filter(pk=pk)
                        work_preference.update(**hot[index])
                    else:
                        work_preference = cp_models.ParameterWorkPreference(language=language, **hot[index])
                        work_preference.save()
                else:
                    work_preference = cp_models.ParameterWorkPreference.objects.filter(pk = pk)
                    work_preference.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def keywords_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/keywords.html')
    
    raise Http404

def keywords_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            keywords = cp_models.ParameterKeyword.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(keywords))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def keywords_save(request):
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
                        keywords = cp_models.ParameterKeyword.objects.filter(pk=pk)
                        keywords.update(**hot[index])
                    else:
                        keywords = cp_models.ParameterKeyword(language=language, **hot[index])
                        keywords.save()
                else:
                    keywords = cp_models.ParameterKeyword.objects.filter(pk = pk)
                    keywords.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def faq_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/faq.html')
    
    raise Http404

def faq_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            faq = cp_models.ParameterFAQ.objects.filter(language=language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(faq))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def faq_save(request):
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
                        faq = cp_models.ParameterFAQ.objects.filter(pk=pk)
                        faq.update(**hot[index])
                    else:
                        faq = cp_models.ParameterFAQ(language=language, **hot[index])
                        faq.save()
                else:
                    faq = cp_models.ParameterFAQ.objects.filter(pk = pk)
                    faq.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404