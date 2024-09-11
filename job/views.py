from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Value, Count, Case, When, CharField
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.conf import settings
from datetime import timedelta

from job.models import Vacancy, Bookmark, Apply, EmployerAction, CandidateAction
from job.utils import vacancy_with_related_info, get_vacancies_context
from recruitment_cp.utils import is_ajax
from .utils import fetch_vacancies
from recruitment_cp.models import ParameterKeyword
from dashboard.decorators import is_candidate, is_employer
from language.utils import tr

import json

# Create your views here.

def vacancies(request):
    vacancies = fetch_vacancies(request)
    
    context = {
        **vacancies,
    }

    return render(request, 'job/vacancies.html', context)

def vacancy(request, slug):
    common_params = {
        'status': True,
        'delete': False,
        'approval_level': 'PUBLISHED'
    }
    vacancy = get_object_or_404(vacancy_with_related_info(Vacancy.translation()), slug=slug, **common_params)
    vacancy.views += 1
    vacancy.save()

    # get related vacancies
    related_vacancies = vacancy_with_related_info(
        Vacancy.translation().filter(job_title=vacancy.job_title, **common_params).exclude(slug=slug)[:5]
    )

    keyword_list = ParameterKeyword.translation().values('id', 'name')
    keywords = {item['id']: item['name'] for item in keyword_list}
    
    context = {
        'vacancy': vacancy,
        'vacancies': related_vacancies,
        'keywords': keywords
    }

    return render(request, 'job/vacancy.html', context)

def categories(request):
    return render(request, 'job/categories.html')

@is_employer
def vacancy_applications(request, slug):
    vacancy = get_object_or_404(Vacancy, slug=slug, approval_level='PUBLISHED')
    applicants = vacancy.applications.select_related('candidate__user').annotate(
        full_name=Concat(
            F('candidate__user__first_name'),
            Value(' '),
            F('candidate__user__last_name')
        ),
        username=F('candidate__user__username')
    ).order_by('-created_date')

    paginator = Paginator(applicants, 30)
    current_page = request.GET.get('page')
    applicants = paginator.get_page(current_page)

    applicants_count = vacancy.applications.count()

    context = {
        'applicants': applicants,
        'applicants_count': applicants_count
    }

    return render(request, 'job/applicants.html', context)

@is_candidate
def applications(request):
    language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
    applications = request.user.candidate.applications.select_related('vacancy').annotate(
        username=F('vacancy__employer__user__username'),
        company_name=F('vacancy__employer__user__first_name'),
        position_title=F('vacancy__position_title'),
        salary_minimum=F('vacancy__salary_minimum'),
        salary_maximum=F('vacancy__salary_maximum'),
        slug=F('vacancy__slug'),
        location=Case(
            When(**{f"vacancy__location__name_{language}__isnull":False},
                then=F(f'vacancy__location__name_{language}')),
                default=Value(''),
                output_field=CharField()
            )
    ).order_by('-created_date')

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
    vacancy = Vacancy.objects.get(id=vacancy, approval_level='PUBLISHED')
    context = dict()

    apply_exists = Apply.objects.filter(candidate=request.user.candidate, vacancy=vacancy).exists()

    if apply_exists:
        apply = Apply.objects.get(
            candidate=request.user.candidate,
            vacancy=vacancy
        )
        apply_id = apply.id
        apply.delete()
        
        context['apply_now_text'] = tr('Apply Now')

    else:
        apply = Apply.objects.create(
            candidate=request.user.candidate,
            vacancy=vacancy,
            message=message,
            cv=cv
        )
        apply_id = apply.id

        context['delete_application_text'] = tr('Delete Application')

    context['apply_id'] = apply_id

    return JsonResponse(context)


@is_employer
def job_postings(request):
    filter_orderby = request.GET.get('orderby')
    url:str = '' # Creating URL for Pagination
    params = {'status': True, 'delete': False} # Default Active selected
    
    if filter_orderby:
        url += f'orderby={filter_orderby}'

        if filter_orderby == 'deactivate':
            params.update({'status': False, 'delete': False})

        elif filter_orderby == 'delete':
            params.update({'delete': True})

    vacancies = vacancy_with_related_info(request.user.employer.vacancies.filter(**params))
    vacancy_count = vacancies.count()

    paginator = Paginator(vacancies, 30)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    context = {
        'vacancies': vacancies,
        'vacancy_count': vacancy_count,
        'url': url
    }

    return render(request, 'job/job-postings.html', context)

@require_POST
def ajax_filter_job_postings(request):
    filter_orderby = request.POST.get('filter_orderby')
    params = {}

    if filter_orderby:
        if filter_orderby == 'active':
            params.update({'status': True, 'delete': False})

        elif filter_orderby == 'deactivate':
            params.update({'status': False, 'delete': False})

        elif filter_orderby == 'delete':
            params.update({'delete': True})

    vacancies = vacancy_with_related_info(request.user.employer.vacancies.filter(**params)).annotate(
        application_count = Count('applications')
    ).order_by('id')
    vacancy_count = vacancies.count()

    paginator = Paginator(vacancies, 30)
    current_page_number = request.POST.get('page', 1)
    vacancies_page = paginator.get_page(current_page_number)

    # serialize data
    vacancies_list = list(vacancies_page.object_list.values())

    pagination_info = {
        'has_next': vacancies_page.has_next(),
        'has_previous': vacancies_page.has_previous(),
        'num_pages': vacancies_page.paginator.num_pages,
        'current_page': vacancies_page.number,
    }

    context = {
        'vacancies': vacancies_list,
        'pagination': pagination_info,
        'vacancy_count': vacancy_count
    }

    return JsonResponse(context, safe=False)

@login_required
def bookmarks(request):
    bookmarks = Bookmark.translation().filter(user=request.user).select_related('user', 'vacancy').annotate(
        username=F('vacancy__employer__user__username'),
        profile_photo=F('vacancy__employer__user__profile_photo'),
        company_name=F('vacancy__employer__user__first_name'),
        position_title=F('vacancy__position_title'),
        salary_minimum=F('vacancy__salary_minimum'),
        salary_maximum=F('vacancy__salary_maximum'),
        slug=F('vacancy__slug'),

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
        params = {
            'status': True, 
            'delete': False,
            'approval_level': 'PUBLISHED'
        }

        if salary_range_lower := data.get('salary_range_lower'):
            params['salary__gte'] = salary_range_lower

        if salary_range_upper := data.get('salary_range_upper'):
            params['salary__lte'] = salary_range_upper

        if work_experiences := data.get('work_experiences'):
            params['work_experience_name__in'] = work_experiences

        if employment_type := data.get('employment_type'):
            params['employment_type_name__in'] = employment_type    

        if sector := data.get('sector'):
            params['employer_sector'] = sector

        if department := data.get('department'):
            params['department_name__in'] = department

        if work_preference := data.get('work_preference'):
            params['work_preference_name__in'] = work_preference

        if career_type := data.get('career_type'):
            params['career_type_name__in'] = career_type

        if date := data.get('date_posted'):
            params['created_date__gte'] = timezone.now() - timedelta(hours=int(date))

        if keyword := data.get('keyword'):
            params['keywords__in'] = keyword

        if location := data.get('location'):
            params['location_name'] = location

        if job_family := data.get('job_family'):
            params['job_title__job_family'] = job_family

        if trending := data.get('trending'):
            params['job_title_name'] = trending

        context = get_vacancies_context(request, Vacancy.translation_for_filter().filter(**params))

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
def ajax_search_vacancy(request):
    query = request.POST.get('search_value', '')

    filtered_vacancies = vacancy_with_related_info(
        Vacancy.translation_for_filter().filter(
            Q(position_title__icontains=query) |
            Q(job_title_name__icontains=query) |
            Q(employer__user__first_name__icontains=query),
            status=True,
            delete=False,
            approval_level='PUBLISHED'
        )
    )

    context = get_vacancies_context(request, filtered_vacancies)

    return JsonResponse(context, safe=False)


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


@is_employer
@require_POST
def ajax_send_employer_action(request):
    applicant_id = request.POST.get('applicant_id')
    action = request.POST.get('action_value')
    invite_date = request.POST.get('invite_date')

    apply_exists = Apply.objects.filter(id=applicant_id).exists()

    if apply_exists:
        employer_action_exists = EmployerAction.objects.filter(apply=applicant_id).exists()

        if action != 'ACCEPT_REQUEST_OTHER_DATE':
            try:
                # delete related candidate action
                CandidateAction.objects.get(apply=applicant_id).delete()

            except ObjectDoesNotExist: ...

        if employer_action_exists:
            EmployerAction.objects.filter(apply=applicant_id).update(
                action=action,
                invite_date=invite_date
            )
        else:
            apply = Apply.objects.get(id=applicant_id)
            EmployerAction.objects.create(
                apply=apply,
                action=action,
                invite_date=invite_date
            )

    return JsonResponse({'status': 'success'})


@is_candidate
@require_POST
def ajax_send_candidate_action(request):
    applicant_id = request.POST.get('applicant_id')
    action = request.POST.get('action_value')
    request_other_date = request.POST.get('request_other_date')

    apply_exists = Apply.objects.filter(id=applicant_id).exists()

    if apply_exists:
        candidate_action_exists = CandidateAction.objects.filter(apply=applicant_id).exists()

        if candidate_action_exists:
            CandidateAction.objects.filter(apply=applicant_id).update(
                action=action,
                request_other_date=request_other_date
            )
        else:
            apply = Apply.objects.get(id=applicant_id)
            CandidateAction.objects.create(
                apply=apply,
                action=action,
                request_other_date=request_other_date
            )

    return JsonResponse({'status': 'success'})