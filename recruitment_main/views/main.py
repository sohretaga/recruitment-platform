from django.shortcuts import render
from recruitment_cp.models import ParameterCareerType, ParameterCareerLevel, ParameterLocation, ParameterFTE, ParameterEmployeeType, ParameterVacancy

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
    pass