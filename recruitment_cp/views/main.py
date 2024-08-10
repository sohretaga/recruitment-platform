from django.shortcuts import render
from django.http import JsonResponse, Http404 
from recruitment_cp.utils import is_ajax
from recruitment_cp import models as cp_models

import json

def index(request):
    if request.user.is_superuser:
        return render(request, 'cp/index.html')
    
    raise Http404

def load_source(request):
    if request.user.is_superuser:
        if is_ajax(request) and request.POST:
            language = request.POST.get('language', None)
            source_model = request.POST.get('model')
            params = {}

            if language:
                params.update({'language_code': language})
            
            match source_model:
            
                case 'career_types':
                    source = cp_models.ParameterCareerType.language_filter(**params).values_list('name', flat=True)

                case 'career_levels':
                    source = cp_models.ParameterCareerLevel.language_filter(**params).values_list('name', flat=True)

                case 'locations':
                    source = cp_models.ParameterLocation.language_filter(**params).values_list('name', flat=True)
                
                case 'fte':
                    source = cp_models.ParameterFTE.language_filter(**params).values_list('name', flat=True)
                
                case 'employment_type':
                    source = cp_models.ParameterEmployeeType.language_filter(**params).values_list('name', flat=True)
                
                case 'work_experience':
                    source = cp_models.ParameterWorkExperience.language_filter(**params).values_list('name', flat=True)
                
                case 'sector':
                    source = cp_models.ParameterSector.language_filter(**params).values_list('name', flat=True)
                
                case 'organization_type':
                    source = cp_models.ParameterOrganizationType.language_filter(**params).values_list('name', flat=True)
                
                case 'organization_ownership':
                    source = cp_models.ParameterOrganizationOwnership.language_filter(**params).values_list('name', flat=True)
                
                case 'number_of_employees':
                    source = cp_models.ParameterNumberOfEmployee.language_filter(**params).values_list('name', flat=True)
                
                case 'work_preference':
                    source = cp_models.ParameterWorkPreference.language_filter(**params).values_list('name', flat=True)
                
                case 'department':
                    source = cp_models.ParameterDepartment.language_filter(**params).values_list('name', flat=True)

                case 'job_family':
                    source = cp_models.ParameterJobFamily.language_filter(**params).values_list('name', flat=True)
            
            source = json.dumps(list(source))
            return JsonResponse(source, safe=False)
        
        else:
            raise PermissionError
    else:
        raise Http404