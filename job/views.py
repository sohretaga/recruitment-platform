from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import F
from datetime import timedelta

from job.models import Vacancy, Bookmark, Apply
from job.utils import vacancy_with_related_info
from recruitment_cp.utils import is_ajax
from .utils import fetch_vacancies
from recruitment_cp.models import ParameterKeyword
from dashboard.decorators import is_candidate, is_employer

import json

# Create your views here.

def vacancies(request):
    vacancies = fetch_vacancies(request)
    
    context = {
        **vacancies,
    }

    return render(request, 'job/vacancies.html', context)

def vacancy(request, slug):
    vacancy = get_object_or_404(vacancy_with_related_info(Vacancy.objects), slug=slug, status=True)
    vacancy.views += 1
    vacancy.save()

    # get related vacancies
    related_vacancies = vacancy_with_related_info(
        Vacancy.objects.filter(job_title=vacancy.job_title, status=True).exclude(slug=slug)[:5]
    )

    keywords = ParameterKeyword.objects.all()
    
    context = {
        'vacancy': vacancy,
        'vacancies': related_vacancies,
        'keywords': keywords
    }

    return render(request, 'job/vacancy.html', context)

def categories(request):
    return render(request, 'job/categories.html')

@is_candidate
def applications(request):
    applications = request.user.candidate.applications.select_related('vacancy', 'candidate').annotate(
        username=F('candidate__user__username'),
        company_name=F('vacancy__employer__user__first_name'),
        position_title=F('vacancy__position_title'),
        location=F('vacancy__location__name'),
        salary_minimum=F('vacancy__salary_minimum'),
        salary_maximum=F('vacancy__salary_maximum'),
        slug=F('vacancy__slug'),
    ).values('username', 'company_name', 'position_title', 'location', 'salary_minimum', 'salary_maximum', 'slug').order_by('created_date')

    paginator = Paginator(applications, 30)
    current_page = request.GET.get('page')
    applications = paginator.get_page(current_page)
    
    context = {
        'applications': applications
    }

    return render(request, 'job/applications.html', context)

@require_POST
@is_candidate
def ajax_apply(request):
    vacancy = request.POST.get('vacancy')
    message = request.POST.get('message')
    cv = request.FILES.get('cv')
    vacancy = Vacancy.objects.get(id=vacancy)

    apply_exists = Apply.objects.filter(candidate=request.user.candidate, vacancy=vacancy).exists()

    if apply_exists:
        Apply.objects.filter(candidate=request.user.candidate, vacancy=vacancy).delete()
        return JsonResponse({'status': 'success', 'message': 'Apply removed'})
    else:
        Apply.objects.create(candidate=request.user.candidate, vacancy=vacancy, message=message, cv=cv)
        return JsonResponse({'status': 'success', 'message': 'Bookmark removed'})


@is_employer
def job_postings(request):
    vacancies = vacancy_with_related_info(request.user.employer.vacancies.all())
    vacancy_count = request.user.employer.vacancies.count()

    paginator = Paginator(vacancies, 30)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    context = {
        'vacancies': vacancies,
        'vacancy_count': vacancy_count
    }

    return render(request, 'job/job-postings.html', context)

@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('user', 'vacancy').annotate(
        username=F('vacancy__employer__user__username'),
        profile_photo=F('vacancy__employer__user__profile_photo'),
        company_name=F('vacancy__employer__user__first_name'),
        position_title=F('vacancy__position_title'),
        work_experience=F('vacancy__work_experience__name'),
        location=F('vacancy__location__name'),
        salary_minimum=F('vacancy__salary_minimum'),
        salary_maximum=F('vacancy__salary_maximum'),
        slug=F('vacancy__slug')
    ).order_by('id')

    bookmark_count = bookmarks.count()

    paginator = Paginator(bookmarks, 30)
    current_page = request.GET.get('page')
    bookmarks = paginator.get_page(current_page)

    context = {
        'bookmarks': bookmarks,
        'bookmark_count': bookmark_count
    }

    return render(request, 'job/bookmarks.html', context)

@require_POST
def ajax_filter_vacancies(request):
    if is_ajax:
        data = json.loads(request.body.decode('utf-8'))
        salary_range_lower:str|None = data.get('salary_range_lower')
        salary_range_upper:str|None = data.get('salary_range_upper')
        work_experiences:str|None = data.get('work_experiences')
        employment_type:str|None = data.get('employment_type')
        sector:str|None = data.get('sector')
        department:str|None = data.get('department')
        work_preference:str|None = data.get('work_preference')
        date = data.get('date_posted')
        params = {'status': True}

        if salary_range_lower:
            params.update({'salary__gte': salary_range_lower})
        
        if salary_range_upper:
            params.update({'salary__lte': salary_range_upper})

        if work_experiences:
            params.update({'work_experience__name__in': work_experiences})
        
        if employment_type:
            params.update({'employment_type__name__in':employment_type})    

        if sector:
            params.update({'employer__sector': sector})

        if department:
            params.update({'department__name__in': department})

        if work_preference:
            params.update({'work_preference__name__in': work_preference})
        
        if date:
            params.update({'created_date__gte': timezone.now() - timedelta(hours=int(date))})

        filtered_vacancies = vacancy_with_related_info(Vacancy.objects.filter(**params))
        # Set up Paginator
        paginator = Paginator(filtered_vacancies, 10)
        current_page_number = request.POST.get('page', 1)
        vacancies_page = paginator.get_page(current_page_number)

        # Serialize the data
        vacancies_list = list(vacancies_page.object_list.values())
        bookmarks = list(Bookmark.objects.filter(user=request.user).values_list('vacancy__id', flat=True))
        keywords = list(ParameterKeyword.objects.all().values('id', 'name'))

        pagination_info = {
            'has_next': vacancies_page.has_next(),
            'has_previous': vacancies_page.has_previous(),
            'num_pages': vacancies_page.paginator.num_pages,
            'current_page': vacancies_page.number,
        }

        context = {
            'vacancies': vacancies_list,
            'pagination': pagination_info,
            'bookmarks': bookmarks,
            'keywords': keywords
        }

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_POST
def ajax_add_bookmark(request):
    vacancy = request.POST.get('vacancy')
    vacancy = Vacancy.objects.get(id=vacancy)
    bookmark_exists = Bookmark.objects.filter(user=request.user, vacancy=vacancy).exists()

    if bookmark_exists:
        Bookmark.objects.filter(user=request.user, vacancy=vacancy).delete()
        return JsonResponse({'status': 'success', 'message': 'Bookmark removed'})
    else:
        Bookmark.objects.create(user=request.user, vacancy=vacancy)
        return JsonResponse({'status': 'success', 'message': 'Bookmark added'})