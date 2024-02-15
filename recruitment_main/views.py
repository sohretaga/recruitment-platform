from django.shortcuts import render
from django.http import JsonResponse
from recruitment_cp.models import ParameterCareerType, ParameterCareerLevel, ParameterLocation, ParameterFTE, ParameterEmployeeType, ParameterVacancy
from django.core import serializers

from ast import literal_eval

# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def contact(request):
    if request.POST:
        ...

    return render(request, 'main/contact.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def team(request):
    return render(request, 'main/team.html')

def pricing(request):
    return render(request, 'main/pricing.html')

def privacy_policy(request):
    return render(request, 'main/privacy-policy.html')

def faqs(request):
    return render(request, 'main/faqs.html')