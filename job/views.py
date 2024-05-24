from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from recruitment_cp import models
from recruitment_cp.functions import is_ajax, datetime_to_string

import json

# Create your views here.

def vacancies(request):
    return render(request, 'job/vacancies.html')

def vacancy(request):
    return render(request, 'job/vacancy.html')

def categories(request):
    return render(request, 'job/categories.html')

def manage_jobs(request):
    return render(request, 'job/manage-jobs.html')

def bookmarks(request):
    return render(request, 'job/bookmarks.html')

@require_POST
def ajax_filter_vacancies(request):
    if is_ajax and request.POST:
        data = json.loads(request.body.decode('utf-8'))
        salary_range = data.get('salary_range', 0)
        work_experiences = data.get('work_experiences', [])
        employment_type = data.get('employment_type', [])

        params = {}
        if salary_range:
            params.update({'salary__lte': salary_range})

        if work_experiences:
            params.update({'work_experience__in': work_experiences})
        
        if employment_type:
            params.update({'employment_type__in':employment_type})        

        filtered_vacancies = models.ParameterVacancy.objects.filter(**params)\
        .values('id', 'no', 'organization', 'career_type', 'career_level', 'location', 'fte', 'salary_minimum',
                'salary_midpoint', 'salary_maximum', 'salary', 'job_catalogue', 'position_title', 'job_title',
                'employment_type', 'work_experience', 'definition', 'created_date')
        
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

def ajax_work_experiences(request):
    ...

def ajax_employment_type(request):
    ...