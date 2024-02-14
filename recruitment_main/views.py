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


def contact(request):
    if request.POST:
        ...

    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')