from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from threading import Thread

from job.utils import fetch_vacancies
from user.models import Employer
from job.models import Vacancy
from recruitment_cp.models import ParameterFAQ, ParameterKeyword
from main.models import FAQ
from blog.models import Blog
from .utils import get_vacancy_in_sublists, mark_notifications_as_read, humanize_time

import json

# Create your views here.

def index(request):
    vacancies = fetch_vacancies(request)
    company_slider = Employer.objects.filter(slider=True, user__profile_photo__isnull=False).exclude(user__profile_photo='')
    today_releases = Vacancy.objects.filter(status=True, delete=False).order_by('?')[:6]
    quick_career_tips = Blog.objects.filter(status='published', quick_career_tip=True)
    featured_slider_vacancies = get_vacancy_in_sublists()
    trending_keywords = ParameterKeyword.objects.filter(trending=True).values('id', 'name')
    
    context = {
        **vacancies,
        'company_slider': company_slider,
        'today_releases': today_releases,
        'featured_slider': featured_slider_vacancies,
        'quick_career_tips': quick_career_tips,
        'trending_keywords': trending_keywords
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


@require_POST
def get_notifications(request):
    thread = Thread(target=mark_notifications_as_read, args=(request,))
    thread.start()

    notifications_list = []
    notifications = request.user.notifications_received.all()[:10]

    for notification in notifications:
        related_object = notification.related_object
        vacancy_slug = related_object.vacancy.slug if related_object else False

        related_data = {
            'user_type': notification.to_user.user_type,
            'profile_photo': notification.from_user.profile_photo,
            'content': notification.content,
            'vacancy_slug': vacancy_slug,
            'timestamp': humanize_time(notification.timestamp)
        }

        notifications_list.append(related_data)

    context = {
        'notifications': json.dumps(notifications_list, default=str)
    }

    return JsonResponse(context, safe=False)