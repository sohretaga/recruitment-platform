from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from threading import Thread

from job.utils import fetch_vacancies
from user.models import Employer
from job.models import Vacancy
from recruitment_cp.models import ParameterFAQ, ParameterKeyword
from main.models import FAQ
from blog.models import Blog
from main.models import Notification, Subscribe, HowItWork, Team, Service, AboutUs, AboutSectionFactor
from .forms import ContactForm
from .utils import get_vacancy_in_sublists, mark_notifications_as_read, fetch_notifications, send_contact_email

import json

# Create your views here.

def index(request):
    vacancies = fetch_vacancies(request)
    company_slider = Employer.objects.filter(slider=True, user__profile_photo__isnull=False).exclude(user__profile_photo='')
    today_releases = Vacancy.translation().filter(status=True, delete=False, approval_level='PUBLISHED').order_by('?')[:6]
    quick_career_tips = Blog.translation().filter(status='published', quick_career_tip=True)
    featured_slider_vacancies = get_vacancy_in_sublists()
    trending_keywords = ParameterKeyword.translation().filter(trending=True).values('id', 'name')
    how_it_works = HowItWork.translation()
    
    context = {
        **vacancies,
        'company_slider': company_slider,
        'today_releases': today_releases,
        'featured_slider': featured_slider_vacancies,
        'quick_career_tips': quick_career_tips,
        'trending_keywords': trending_keywords,
        'how_it_works': how_it_works
    }

    return render(request, 'main/index.html', context)

def contact(request):
    context = {
        'submitted': False
    }

    if request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            context['submitted'] = True
            
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            send_contact_email(name, email, subject, message)

    return render(request, 'main/contact.html', context)

def about(request):

    try:
        about_section = AboutUs.objects.get(section='ABOUT_SECTION')
        about_section = about_section.about_section.translation()[0]

    except AboutUs.DoesNotExist:
        about_section = list()

    try:
        about_section_factors = AboutUs.objects.get(section='ABOUT_SECTION_FACTORS')
        about_section_factors = AboutSectionFactor.translation().filter(about_section=about_section_factors)

    except AboutUs.DoesNotExist:
        about_section_factors = list()

    context = {
        'about_section': about_section,
        'about_section_factors': about_section_factors
    }
    
    return render(request, 'main/about.html', context)

def services(request):
    services = Service.translation()
    context = {
        'services': services
    }

    return render(request, 'main/services.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service.translation(), slug=slug)
    services = Service.translation().exclude(slug=slug)

    context = {
        'service': service,
        'services': services
    }

    return render(request, 'main/service-detail.html', context)

def team(request):
    team = Team.translation()
    context = {
        'team': team
    }
    return render(request, 'main/team.html', context)

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

@require_POST
def get_notifications(request):
    thread = Thread(target=mark_notifications_as_read, args=(request,))
    thread.start()

    notifications = fetch_notifications(request.user.notifications_received.all()[:10])

    context = {
        'notifications': json.dumps(notifications, default=str)
    }

    return JsonResponse(context, safe=False)

def notifications(request):
    notifications = fetch_notifications(request.user.notifications_received.all())

    paginator = Paginator(notifications, 30)
    current_page = request.GET.get('page', 1)
    notifications = paginator.get_page(current_page)

    context = {
        'notifications': notifications
    }

    return render(request, 'main/notifications.html', context)

@require_POST
def delete_notifications(request):
    id_list = json.loads(request.POST.get('id_list'))
    notifications = Notification.objects.filter(id__in=id_list)
    notifications.delete()

    return JsonResponse({'status':200})

@require_POST
def delete_notification(request):
    notification_id = request.POST.get('notification_id')
    notifications = Notification.objects.filter(id=notification_id)
    notifications.delete()
    
    return JsonResponse({'status':200})

@require_POST
def subscribe(request):
    email = request.POST.get('email')
    Subscribe.objects.create(email=email)

    return JsonResponse({'status': 200})


@require_POST
def set_language(request):
    data = json.loads(request.body)
    language_code = data.get('language', settings.SITE_LANGUAGE_CODE)
    cache.set(f'site_language', language_code, timeout=604800)
    return JsonResponse({'status': 'success'})