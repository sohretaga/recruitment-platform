from django.shortcuts import render
from django.http import JsonResponse, Http404 
from recruitment_cp.functions import is_ajax
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
            source_model = request.POST.get('model')
            
            if source_model == 'career_types':
                source = cp_models.ParameterCareerType.objects.filter(language = language).values_list('name', flat=True)

            elif source_model == 'career_levels':
                source = cp_models.ParameterCareerLevel.objects.filter(language = language).values_list('name', flat=True)

            elif source_model == 'locations':
                source = cp_models.ParameterLocation.objects.filter(language = language).values_list('name', flat=True)
            
            elif source_model == 'fte':
                source = cp_models.ParameterFTE.objects.filter(language = language).values_list('name', flat=True)
            
            elif source_model == 'employment_type':
                source = cp_models.ParameterEmployeeType.objects.filter(language = language).values_list('name', flat=True)
            
            source = json.dumps(list(source))
            return JsonResponse(source, safe=False)
        
        else:
            raise PermissionError
    else:
        raise Http404