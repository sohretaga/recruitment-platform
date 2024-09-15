from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone

from dashboard.decorators import is_controller
from job.models import Vacancy
from job.utils import vacancy_with_related_info
from user.tasks import send_notification_to_preferred_candidates
from datetime import timedelta

@is_controller
def all_vacancies(request):
    all_vacancies_count = Vacancy.objects.count()

    context = {
        'all_vacancies_count': all_vacancies_count
    }

    return render(request, 'dashboard/controller/all-vacancies.html', context)

@is_controller
def ajax_all_vacancies(request):
    start:str = int(request.GET.get('start', 0))
    length:str = int(request.GET.get('length', 10))
    search_value:str = request.GET.get('search[value]', '')

    vacancies = vacancy_with_related_info(Vacancy.translation().all())

    if search_value:
        vacancies = vacancies.filter(position_title__icontains=search_value)

    paginator = Paginator(vacancies, length)
    page_number = (start // length) + 1
    page_vacancies = paginator.get_page(page_number)

    data = []
    for obj in page_vacancies:
        data.append([
            obj.position_title,
            obj.job_title_name,
            obj.career_type_name,
            obj.career_level_name,
            obj.salary_minimum,
            obj.salary_midpoint,
            obj.salary_maximum,
            obj.salary,
            obj.views,
            obj.id,
            obj.slug,
            obj.status,
            obj.approval_level,
            obj.type
        ])

    response = {
        "draw": request.GET.get('draw', 1),
        "recordsTotal": paginator.count,
        "recordsFiltered": paginator.count,
        "data": data,
    }

    return JsonResponse(response)

@is_controller
def ajax_manage_approval_level(request):
    vacancy_id = request.POST.get('vacancy_id')
    approval_level = request.POST.get('approval_level')
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    vacancy.approval_level = approval_level
    published_date = True

    if approval_level == 'PUBLISHED':
        ws_protocol = 'wss://' if request.is_secure() else 'ws://'
        host = request.get_host()
        send_notification_to_preferred_candidates.delay(vacancy.id, ws_protocol, host)

        if not vacancy.published_date:
            vacancy.published_date = timezone.now()
            vacancy.ending_date = vacancy.published_date + timedelta(days=30)
            published_date = False

    vacancy.save()

    context = {
        'published_date': published_date
    }

    return JsonResponse(context)

@is_controller
def ajax_update_published_date(request):
    vacancy_id = request.POST.get('vacancy_id')
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    
    vacancy.published_date = timezone.now()
    vacancy.ending_date = vacancy.published_date + timedelta(days=30)
    vacancy.save()

    return JsonResponse({'status':200})

@is_controller
def ajax_manage_type(request):
    vacancy_id = request.POST.get('vacancy_id')
    type = request.POST.get('type')
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    vacancy.type = type
    vacancy.save()
    return JsonResponse({'status': 200})