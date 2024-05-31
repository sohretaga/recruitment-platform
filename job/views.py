from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from recruitment_cp import models
from recruitment_cp.utils import is_ajax
from .utils import fetch_vacancies

import json

# Create your views here.

def vacancies(request):
    vacancies = fetch_vacancies(request)

    context = {
        **vacancies
    }

    return render(request, 'job/vacancies.html', context)

def vacancy(request, slug):
    vacancy = get_object_or_404(models.ParameterVacancy, slug=slug)
    vacancy.views += 1
    vacancy.save()

    context = {
        'vacancy': vacancy
    }

    return render(request, 'job/vacancy.html', context)

def categories(request):
    return render(request, 'job/categories.html')

def manage_jobs(request):
    return render(request, 'job/manage-jobs.html')

def bookmarks(request):
    return render(request, 'job/bookmarks.html')

@require_POST
def ajax_filter_vacancies(request):
    if is_ajax:
        data = json.loads(request.body.decode('utf-8'))
        salary_range_lower = data.get('salary_range_lower', 0)
        salary_range_upper = data.get('salary_range_upper', 0)
        work_experiences = data.get('work_experiences', [])
        employment_type = data.get('employment_type', [])

        params = {}
        if salary_range_lower:
            params.update({'salary__gte': salary_range_lower})
        
        if salary_range_upper:
            params.update({'salary__lte': salary_range_upper})

        if work_experiences:
            params.update({'work_experience__in': work_experiences})
        
        if employment_type:
            params.update({'employment_type__in':employment_type})        

        filtered_vacancies = models.ParameterVacancy.objects.filter(**params)\
        .values('id', 'no', 'employer__company_name', 'career_type', 'career_level', 'location', 'fte',
                'salary_minimum', 'salary_midpoint', 'salary_maximum', 'salary', 'position_title', 'job_title',
                'employment_type', 'work_experience', 'definition', 'slug', 'created_date')
        
        # Set up Paginator
        paginator = Paginator(filtered_vacancies, 10)
        current_page_number = request.POST.get('page', 1)
        vacancies_page = paginator.get_page(current_page_number)

        # Serialize the data
        vacancies_list = list(vacancies_page.object_list.values())

        pagination_info = {
            'has_next': vacancies_page.has_next(),
            'has_previous': vacancies_page.has_previous(),
            'num_pages': vacancies_page.paginator.num_pages,
            'current_page': vacancies_page.number,
        }

        context = {
            'vacancies': vacancies_list,
            'pagination': pagination_info
        }

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)