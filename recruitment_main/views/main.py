from django.shortcuts import render
from django.http import JsonResponse
from recruitment_cp.models import ParameterCareerType, ParameterCareerLevel, ParameterLocation, ParameterFTE, ParameterEmployeeType, ParameterVacancy
from django.core import serializers

from ast import literal_eval

# Create your views here.

def index(request):
    career_types = ParameterCareerType.objects.all()
    career_levles = ParameterCareerLevel.objects.all()
    locations = ParameterLocation.objects.all()
    fte = ParameterFTE.objects.all()
    employment_types = ParameterEmployeeType.objects.all()
    vacancies = ParameterVacancy.objects.all()

    context = {
        'career_types': career_types,
        'career_levels': career_levles,
        'locations': locations,
        'fte': fte,
        'employment_types': employment_types,
        'vacancies': vacancies,
    }

    return render(request, 'main/index.html', context)

def vacancy_load(request):
    career_type = request.POST.get('career_type')
    career_level = request.POST.get('career_level')
    location = request.POST.get('location')
    fte = request.POST.get('fte')
    employee_type = literal_eval(request.POST.get('employee_type'))

    filters = {}

    if career_type != '---':
        filters['career_type'] = career_type
    
    if career_level != '---':
        filters['career_level'] = career_level

    if location != '---':
        filters['location'] = location

    if fte != '---':
        filters['fte'] = fte

    vacancies = ParameterVacancy.objects.filter(**filters, employee_type__in = employee_type)

    vacancies_json = serializers.serialize('json', vacancies)

    context = {
        'vacancies': vacancies_json
    }

    return JsonResponse(context)