from django.shortcuts import render
from recruitment_cp.models import ParameterCareerType, ParameterCareerLevel, ParameterLocation, ParameterFTE, ParameterEmployeeType

# Create your views here.

def index(request):
    career_types = ParameterCareerType.objects.all()
    career_levles = ParameterCareerLevel.objects.all()
    locations = ParameterLocation.objects.all()
    fte = ParameterFTE.objects.all()
    employment_types = ParameterEmployeeType.objects.all()

    context = {
        'career_types': career_types,
        'career_levels': career_levles,
        'locations': locations,
        'fte': fte,
        'employment_types': employment_types,
    }

    return render(request, 'main/index.html', context)