from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from threading import Thread

from job.utils import fetch_vacancies
from user.models import Employer
from job.models import Vacancy
from recruitment_cp.models import ParameterFAQ, ParameterKeyword
from main.models import FAQ
from blog.models import Blog
from main.models import Notification
from .utils import get_vacancy_in_sublists, mark_notifications_as_read, fetch_notifications

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
