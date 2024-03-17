from django.shortcuts import render
from django.http import JsonResponse
from recruitment_cp import models

# Create your views here.

def index(request):
    catalogues = models.ParameterJobCatalogue.objects.filter(language = 'en').values_list('name', flat=True)

    context = {
        'catalogues': catalogues
    }

    return render(request, 'main/index.html', context)


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