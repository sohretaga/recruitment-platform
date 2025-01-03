from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.db.models import F, Case, When, Value, CharField, Count, Q

from recruitment_cp import models as cp_models
from blog.models import Category as BlogCategory
from job.models import Vacancy, ExpiredVacancy
from user.models import Candidate, Employer
from recruitment_cp.utils import is_ajax, datetime_to_string, date_to_string

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
            
            career_types = cp_models.ParameterCareerType.language_filter(language_code=language).values(
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

                if name or language != 'en':
                    if pk:
                        career_types = cp_models.ParameterCareerType.objects.filter(pk=pk)
                        career_types.custom_update(language, **hot[index])
                    else:
                        career_types = cp_models.ParameterCareerType()
                        career_types.save(language=language, **hot[index])
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
            
            career_levels = cp_models.ParameterCareerLevel.language_filter(language_code=language).values(
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

                if name or language != 'en':
                    if pk:
                        career_level = cp_models.ParameterCareerLevel.objects.filter(pk=pk)
                        career_level.custom_update(language, **hot[index])
                    else:
                        career_level = cp_models.ParameterCareerLevel()
                        career_level.save(language=language, **hot[index])
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
            
            career_types_levels = cp_models.ParameterCareerTypeLevel.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        career_types_levels = cp_models.ParameterCareerTypeLevel.objects.filter(pk=pk)
                        career_types_levels.custom_update(language, **hot[index])
                    else:
                        career_types_levels = cp_models.ParameterCareerTypeLevel()
                        career_types_levels.save(language, **hot[index])
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
            
            locations = cp_models.ParameterLocation.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        locations = cp_models.ParameterLocation.objects.filter(pk=pk)
                        locations.custom_update(language, **hot[index])
                    else:
                        locations = cp_models.ParameterLocation()
                        locations.save(language, **hot[index])
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
            
            countries = cp_models.ParameterCountry.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        countries = cp_models.ParameterCountry.objects.filter(pk=pk)
                        countries.custom_update(language, **hot[index])
                    else:
                        countries = cp_models.ParameterCountry()
                        countries.save(language, **hot[index])
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
            
            work_experience = cp_models.ParameterWorkExperience.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'minimum', 'maximum'
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
                minimum = hot[index].get('minimum', 0)
                maximum = hot[index].get('maximum', 0)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        work_experience = cp_models.ParameterWorkExperience.objects.filter(pk=pk)
                        work_experience.custom_update(language, **hot[index])
                    else:
                        work_experience = cp_models.ParameterWorkExperience(minimum=minimum, maximum=maximum)
                        work_experience.save(language, **hot[index])
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
            
            fte = cp_models.ParameterFTE.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        fte = cp_models.ParameterFTE.objects.filter(pk=pk)
                        fte.custom_update(language, **hot[index])
                    else:
                        fte = cp_models.ParameterFTE()
                        fte.save(language, **hot[index])
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
            
            job_catalogues = cp_models.ParameterJobCatalogue.language_filter(language)\
                .values(
                    'id', 'no', 'name', 'definition', 'note', 'job_family_name', 'job_sub_family',
                    'career_type_name', 'career_level', 'typical_education_name', 'relevant_experience_name',
                    'job_code', 'description', 'responsibilities', 'qualification', 'skill_experience'
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
                job_family_name = hot[index].pop('job_family_name')
                career_type_name = hot[index].pop('career_type_name')
                typical_education_name = hot[index].pop('typical_education_name')
                relevant_experience_name = hot[index].pop('relevant_experience_name')

                if name or language != 'en':
                    try:
                        job_family = cp_models.ParameterJobFamily.translation().get(name=job_family_name)
                        hot[index]['job_family'] = job_family
                    except cp_models.ParameterJobFamily.DoesNotExist: ...

                    try:
                        career_type = cp_models.ParameterCareerType.translation().get(name=career_type_name)
                        hot[index]['career_type'] = career_type
                    except cp_models.ParameterCareerType.DoesNotExist: ...

                    try:
                        typical_education = cp_models.ParameterEducationLevel.translation().get(name=typical_education_name)
                        hot[index]['typical_education'] = typical_education
                    except cp_models.ParameterEducationLevel.DoesNotExist: ...

                    try:
                        relevant_experience = cp_models.ParameterWorkExperience.translation().get(name=relevant_experience_name)
                        hot[index]['relevant_experience'] = relevant_experience
                    except cp_models.ParameterWorkExperience.DoesNotExist: ...

                    if pk:
                        job_catalogues = cp_models.ParameterJobCatalogue.objects.filter(pk=pk)
                        job_catalogues.custom_update(language, **hot[index])
                    else:
                        job_catalogues = cp_models.ParameterJobCatalogue()
                        job_catalogues.save(language, **hot[index])
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
            
            employee_type = cp_models.ParameterEmployeeType.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        employee_type = cp_models.ParameterEmployeeType.objects.filter(pk=pk)
                        employee_type.custom_update(language, **hot[index])
                    else:
                        employee_type = cp_models.ParameterEmployeeType()
                        employee_type.save(language, **hot[index])
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
            vacancy_type = request.POST.get('vacancies')
            offset = int(request.POST.get('offset', 0))
            limit = int(request.POST.get('limit', 1000))
            
            match vacancy_type:
                case 'active_vacancies':
                    vacancies = Vacancy.translation().filter(language = language).select_related('employer')\
                        .annotate(
                            company_name=F('employer__user__first_name',
                        ),
                    ).values()[offset:offset+limit]
                
                case 'expired_vacancy':
                    vacancies = ExpiredVacancy.translation().filter(language = language).select_related(
                    'employer').annotate(company_name=F('employer__user__first_name'),
                    ).values()[offset:offset+limit]
                case _:
                    vacancies = {}
            
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
            language = request.POST.get('language')
            
            blog_category = BlogCategory.language_filter(language).values(
                'id', 'name', 'definition', 'note'
            )
            
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

                if name or language != 'en':
                    if pk:
                        blog_category = BlogCategory.objects.filter(pk=pk)
                        blog_category.custom_update(language, **hot[index])
                    else:
                        blog_category = BlogCategory()
                        blog_category.save(language, **hot[index])
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
            
            company = Employer.objects.annotate(
                vacancy_count=Count('vacancies', filter=Q(vacancies__status=True, vacancies__delete=False, vacancies__approval_level='PUBLISHED'))
            ).values(
                'id', 'user__email', 'user__profile_photo', 'no', 'user__first_name',
                'sector__name_en', 'organization_type__name_en', 'organization_ownership__name_en',
                'number_of_employees__name_en', 'second_email', 'other_email', 'note', 'slider',
                'amcham_user', 'key_account','vacancy_count', 'discount_code'
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
                params = {
                    "slider": hot[index].get('slider'),
                    "amcham_user": hot[index].get('amcham_user'),
                    "key_account": hot[index].get('key_account')
                }

                try:
                    params['sector'] = cp_models.ParameterSector.objects.get(name_en=hot[index]['sector__name_en'])
                except cp_models.ParameterSector.DoesNotExist:
                    pass

                try:
                    params['organization_type'] = cp_models.ParameterOrganizationType.objects.get(name_en=hot[index]['organization_type__name_en'])
                except cp_models.ParameterOrganizationType.DoesNotExist:
                    pass

                try:
                    params['organization_ownership'] = cp_models.ParameterOrganizationOwnership.objects.get(name_en=hot[index]['organization_ownership__name_en'])
                except cp_models.ParameterOrganizationOwnership.DoesNotExist:
                    pass

                try:
                    params['number_of_employees'] = cp_models.ParameterNumberOfEmployee.objects.get(name_en=hot[index]['number_of_employees__name_en'])
                except cp_models.ParameterNumberOfEmployee.DoesNotExist:
                    pass

                if pk:
                    company = Employer.objects.filter(pk=pk)
                    company.update(**params)
                else:
                    company = Employer(**hot[index])
                    company.save()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

import random
import string
    
def generate_discount_code(request):
    employers = Employer.objects.filter(discount_code__isnull=True)
    characters = string.ascii_uppercase + string.digits

    for employer in employers:
        employer.discount_code = ''.join(random.choices(characters, k=6))
        employer.save()
    
    return JsonResponse({'status': 200})
    
#======================================================================================================
def candidate_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/candidates.html')
    
    raise Http404

def candidate_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            gender_case = Case(
                When(gender='male', then=Value('Male')),
                When(gender='female', then=Value('Female')),
                output_field=CharField()
            )
            
            candidate = Candidate.translation().select_related('user').annotate(
                first_name=F('user__first_name'),
                last_name=F('user__last_name'),
                username=F('user__username'),
                email=F('user__email'),
                gender_name=gender_case,
            ).values(
                'id', 'first_name', 'last_name', 'username', 'gender_name', 'citizenship_name',
                'birthday', 'age', 'email', 'work_experience_name', 'education_level_name'
            )
            
            json_data = json.dumps(list(candidate), default=date_to_string)

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

                if pk:
                    candidate = Candidate.objects.filter(pk=pk)
                    candidate.update(**hot[index])
                else:
                    candidate = Candidate(**hot[index])
                    candidate.save()
                
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
            
            sector = cp_models.ParameterSector.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        sector = cp_models.ParameterSector.objects.filter(pk=pk)
                        sector.custom_update(language, **hot[index])
                    else:
                        sector = cp_models.ParameterSector()
                        sector.save(language, **hot[index])
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
            
            organization_type = cp_models.ParameterOrganizationType.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        organization_type = cp_models.ParameterOrganizationType.objects.filter(pk=pk)
                        organization_type.custom_update(language, **hot[index])
                    else:
                        organization_type = cp_models.ParameterOrganizationType()
                        organization_type.save(language, **hot[index])
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
            
            organization_ownership = cp_models.ParameterOrganizationOwnership.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        organization_ownership = cp_models.ParameterOrganizationOwnership.objects.filter(pk=pk)
                        organization_ownership.custom_update(language, **hot[index])
                    else:
                        organization_ownership = cp_models.ParameterOrganizationOwnership()
                        organization_ownership.save(language, **hot[index])
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
            
            number_of_employees = cp_models.ParameterNumberOfEmployee.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        number_of_employees = cp_models.ParameterNumberOfEmployee.objects.filter(pk=pk)
                        number_of_employees.custom_update(language, **hot[index])
                    else:
                        number_of_employees = cp_models.ParameterNumberOfEmployee()
                        number_of_employees.save(language, **hot[index])
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
            
            department = cp_models.ParameterDepartment.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        department = cp_models.ParameterDepartment.objects.filter(pk=pk)
                        department.custom_update(language, **hot[index])
                    else:
                        department = cp_models.ParameterDepartment()
                        department.save(language, **hot[index])
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
            
            work_preference = cp_models.ParameterWorkPreference.language_filter(language_code=language).values(
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

                if name or language != 'en':
                    if pk:
                        work_preference = cp_models.ParameterWorkPreference.objects.filter(pk=pk)
                        work_preference.custom_update(language, **hot[index])
                    else:
                        work_preference = cp_models.ParameterWorkPreference()
                        work_preference.save(language=language, **hot[index])
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
            
            keywords = cp_models.ParameterKeyword.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'trending'
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

                if name or language != 'en':
                    if pk:
                        keywords = cp_models.ParameterKeyword.objects.filter(pk=pk)
                        keywords.custom_update(language, **hot[index])
                    else:
                        keywords = cp_models.ParameterKeyword()
                        keywords.save(language, **hot[index])
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
            
            faq = cp_models.ParameterFAQ.language_filter(language).values(
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

                if name or language != 'en':
                    if pk:
                        faq = cp_models.ParameterFAQ.objects.filter(pk=pk)
                        faq.custom_update(language, **hot[index])
                    else:
                        faq = cp_models.ParameterFAQ()
                        faq.save(language, **hot[index])
                else:
                    faq = cp_models.ParameterFAQ.objects.filter(pk = pk)
                    faq.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def competence_grouping_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/competence_grouping.html')
    
    raise Http404

def competence_grouping_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            competence_grouping = cp_models.ParameterCompetenceGrouping.language_filter(language).values(
                'id', 'no', 'name', 'key', 'definition', 'note'
            )
            json_data = json.dumps(list(competence_grouping))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def competence_grouping_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        competence_grouping = cp_models.ParameterCompetenceGrouping.objects.filter(pk=pk)
                        competence_grouping.custom_update(language, **hot[index])
                    else:
                        competence_grouping = cp_models.ParameterCompetenceGrouping()
                        competence_grouping.save(language, **hot[index])
                else:
                    competence_grouping = cp_models.ParameterCompetenceGrouping.objects.filter(pk = pk)
                    competence_grouping.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def competence_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/competencies.html')
    
    raise Http404

def competence_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            competence = cp_models.ParameterCompetence.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'grouping_name',
                'behavioral_competence', 'functional_competence', 'it_competence', 'language_competence'
            )
            json_data = json.dumps(list(competence))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def competence_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                grouping_name = hot[index].pop('grouping_name', None)
                if grouping_name:
                    try:
                        grouping = cp_models.ParameterCompetenceGrouping.language_filter(language).get(name=grouping_name)
                        hot[index]['grouping'] = grouping

                    except cp_models.ParameterCompetenceGrouping.DoesNotExist: ...
                
                params = {
                    'behavioral_competence': hot[index].get('behavioral_competence') or False,
                    'functional_competence': hot[index].get('functional_competence') or False,
                    'it_competence': hot[index].get('it_competence') or False,
                    'language_competence': hot[index].get('language_competence') or False
                }

                if name or language != 'en':
                    if pk:
                        competence = cp_models.ParameterCompetence.objects.filter(pk=pk)
                        competence.custom_update(language, **hot[index])

                    else:
                        params['grouping'] = hot[index].get('grouping')
                        competence = cp_models.ParameterCompetence(**params)
                        competence.save(language, **hot[index])
                else:
                    competence = cp_models.ParameterCompetence.objects.filter(pk = pk)
                    competence.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def job_family_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/job_family.html')
    
    raise Http404

def job_family_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            job_family = cp_models.ParameterJobFamily.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note'
            )
            json_data = json.dumps(list(job_family))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def job_family_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        job_family = cp_models.ParameterJobFamily.objects.filter(pk=pk)
                        job_family.custom_update(language, **hot[index])
                    else:
                        job_family = cp_models.ParameterJobFamily()
                        job_family.save(language, **hot[index])
                else:
                    job_family = cp_models.ParameterJobFamily.objects.filter(pk = pk)
                    job_family.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def date_posted_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/date_posted.html')
    
    raise Http404

def date_posted_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            date_posted = cp_models.ParameterDatePosted.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'hours'
            )
            json_data = json.dumps(list(date_posted))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def date_posted_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        date_posted = cp_models.ParameterDatePosted.objects.filter(pk=pk)
                        date_posted.custom_update(language, **hot[index])
                    else:
                        date_posted = cp_models.ParameterDatePosted(hours=hot[index]['hours'])
                        date_posted.save(language, **hot[index])
                else:
                    date_posted = cp_models.ParameterDatePosted.objects.filter(pk = pk)
                    date_posted.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def age_group_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/age_group.html')
    
    raise Http404

def age_group_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            age_group = cp_models.ParameterAgeGroup.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'minimum', 'maximum'
            )
            json_data = json.dumps(list(age_group))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def age_group_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                minimum = hot[index].get('minimum', 0)
                maximum = hot[index].get('maximum', 0)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        age_group = cp_models.ParameterAgeGroup.objects.filter(pk=pk)
                        age_group.custom_update(language, **hot[index])
                    else:
                        age_group = cp_models.ParameterAgeGroup(minimum=minimum, maximum=maximum)
                        age_group.save(language, **hot[index])
                else:
                    age_group = cp_models.ParameterAgeGroup.objects.filter(pk = pk)
                    age_group.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def education_level_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/education_level.html')
    
    raise Http404

def education_level_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            education_level = cp_models.ParameterEducationLevel.language_filter(language).values(
                'id', 'no', 'name', 'definition', 'note', 'level_order'
            )
            json_data = json.dumps(list(education_level))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def education_level_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                level_order = hot[index].get('level_order', 0)
                name = hot[index].get('name', None)

                if name or language != 'en':
                    if pk:
                        education_level = cp_models.ParameterEducationLevel.objects.filter(pk=pk)
                        education_level.custom_update(language, **hot[index])
                    else:
                        education_level = cp_models.ParameterEducationLevel(level_order=level_order)
                        education_level.save(language, **hot[index])
                else:
                    education_level = cp_models.ParameterEducationLevel.objects.filter(pk = pk)
                    education_level.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404

#======================================================================================================
def pricing_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/pricing.html')
    
    raise Http404

def pricing_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            pricing = cp_models.ParameterPricing.language_filter(language).values(
                'id', 'no', 'name', 'standard', 'premium', 'hot_vacancies', 'active'
            )
            json_data = json.dumps(list(pricing))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def pricing_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                standard = hot[index].get('standard', 0)
                premium = hot[index].get('premium', 0)
                hot_vacancies = hot[index].get('hot_vacancies', 0)
                name = hot[index].get('name', None)
                active = hot[index].get('active', False)

                if name or language != 'en':
                    if pk:
                        pricing = cp_models.ParameterPricing.objects.filter(pk=pk)
                        pricing.custom_update(language, **hot[index])
                    else:
                        pricing = cp_models.ParameterPricing(standard=standard, premium=premium, hot_vacancies=hot_vacancies, active=active)
                        pricing.save(language, **hot[index])
                else:
                    pricing = cp_models.ParameterPricing.objects.filter(pk = pk)
                    pricing.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def pricing_external_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/pricing_external.html')
    
    raise Http404

def pricing_external_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            pricing_external = cp_models.ParameterPricingExternal.language_filter(language).values(
                'id', 'name', 'price'
            )
            json_data = json.dumps(list(pricing_external))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def pricing_external_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                name = hot[index].get('name')
                price = hot[index].get('price', 0)

                if name or language != 'en':
                    if pk:
                        pricing_external = cp_models.ParameterPricingExternal.objects.filter(pk=pk)
                        pricing_external.custom_update(language, **hot[index])
                    else:
                        pricing_external = cp_models.ParameterPricingExternal(price=price)
                        pricing_external.save(language, **hot[index])
                else:
                    pricing_external = cp_models.ParameterPricingExternal.objects.filter(pk = pk)
                    pricing_external.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404
    
#======================================================================================================
def pricing_feature_index(request):
    if request.user.is_superuser:
        return render(request, 'cp/parameters/pricing_feature.html')
    
    raise Http404

def pricing_feature_load(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language')
            
            pricing_feature = cp_models.ParameterPricingFeature.language_filter(language).values(
                'id', 'no', 'feature', 'standard', 'premium'
            )
            json_data = json.dumps(list(pricing_feature))

            return JsonResponse(json_data, safe=False)
        else:
            raise PermissionError
    else:
        raise Http404

def pricing_feature_save(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            hot = json.loads(request.POST.get('hot'))
            language = request.POST.get('language')
            index = 0

            while index < len(hot):
                pk = hot[index].pop('id', None)
                no = hot[index].pop('no', None)
                feature = hot[index].get('feature')
                standard = hot[index].get('standard') or False
                premium = hot[index].get('premium') or False

                if feature or language != 'en':
                    if pk:
                        pricing_feature = cp_models.ParameterPricingFeature.objects.filter(pk=pk)
                        pricing_feature.custom_update(language, name=feature, no=no, standard=standard, premium=premium)
                    else:
                        pricing_feature = cp_models.ParameterPricingFeature(no=no, standard=standard, premium=premium)
                        pricing_feature.save(language, name=feature)
                else:
                    pricing_feature = cp_models.ParameterPricingFeature.objects.filter(pk = pk)
                    pricing_feature.delete()
                
                index += 1

            return JsonResponse({'status': 200})
        else:
            raise PermissionError
    else:
        raise Http404