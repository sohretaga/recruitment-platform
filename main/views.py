from django.shortcuts import render
from job.utils import fetch_vacancies
from user.models import Employer

# Create your views here.

def index(request):
    vacancies = fetch_vacancies(request)
    sliders = Employer.objects.filter(slider=True, user__profile_photo__isnull=False).exclude(user__profile_photo='')
    
    context = {
        **vacancies,
        'sliders': sliders
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