from django.shortcuts import render

from job.utils import fetch_vacancies
from user.models import Employer
from job.models import Vacancy
from recruitment_cp.models import ParameterFAQ
from main.models import FAQ

import math

# Create your views here.

def index(request):
    vacancies = fetch_vacancies(request)
    company_slider = Employer.objects.filter(slider=True, user__profile_photo__isnull=False).exclude(user__profile_photo='')

    today_releases = Vacancy.objects.all().order_by('?')[:6]

    def get_objects_in_sublists(objects_per_list=5):
        objects = list(Vacancy.objects.all().order_by('?')[:10])
        
        total_objects = len(objects)
        
        number_of_lists = math.ceil(total_objects / objects_per_list)
        
        sublists = [
            objects[i * objects_per_list:(i + 1) * objects_per_list]
            for i in range(number_of_lists)
        ]
    
        return sublists
    
    
    context = {
        **vacancies,
        'company_slider': company_slider,
        'today_releases': today_releases,
        'featured_slider': get_objects_in_sublists()
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
    categories = ParameterFAQ.objects.all()
    faqs = FAQ.objects.all()

    context = {
        'categories': categories,
        'faqs': faqs
    }

    return render(request, 'main/faqs.html', context)

def coming_soon(request):
    return render(request, 'main/coming-soon.html')