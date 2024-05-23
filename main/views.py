from django.shortcuts import render
from django.core.paginator import Paginator

from recruitment_cp import models

# Create your views here.

def index(request):

    # Set up Paginator
    paginator = Paginator(models.ParameterVacancy.objects.all(), 10)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    # Filter Fields
    countries = models.ParameterCountry.objects.all().values('name')
    experiences = models.ParameterWorkExperience.objects.all().values('id', 'name')
    employments = models.ParameterEmployeeType.objects.all().values('id', 'name')

    context = {
        'vacancies': vacancies,
        'countries': countries,
        'experiences': experiences,
        'employments': employments
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

def coming_soon(request):
    return render(request, 'main/coming-soon.html')