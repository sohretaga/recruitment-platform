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
            language = request.POST.get('language')
            table_map = request.POST.get('map')
            table_map = json.loads(table_map)
            params = {}
            data = {}

            if not language: # set default language if language is not set
                language = 'en'

            params['language_code'] = language

            for source_model in table_map:
            
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
                    
                    case 'education_level':
                        source = cp_models.ParameterEducationLevel.language_filter(**params).values_list('name', flat=True)
                    
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
                    
                    case 'grouping':
                        source = cp_models.ParameterCompetenceGrouping.language_filter(**params).values_list('name', flat=True)

                data[source_model] = json.dumps(list(source))
            
            return JsonResponse(data)
        
        else:
            raise PermissionError
    else:
        raise Http404