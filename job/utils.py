from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import F, Count, When, Case, Value, CharField, BooleanField, Exists, OuterRef
from django.db.models.functions import Concat
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

from recruitment_cp import models
from job.models import Vacancy
from language.utils import tr


def get_vacancies_context(request, vacancies) -> dict:

    # Set up Paginator
    paginator = Paginator(vacancy_with_related_info(vacancies), 10)
    current_page_number = request.POST.get('page', 1)
    vacancies_page = paginator.get_page(current_page_number)
    vacancy_args = [
        'id', 'employer_username', 'profile_photo_url', 'company_name',
        'slug', 'position_title', 'location_name', 'salary_minimum',
        'salary_maximum', 'work_experience_name', 'keywords_names', 'user_id',
        'anonium', 'employer_sector'
    ]

    # Serialize the data
    if request.user.is_authenticated:
        vacancy_args.append('is_bookmarked')
        
        bookmarked_vacancies = request.user.bookmarks.filter(vacancy=OuterRef('pk'))
        applied_vacancies = None

        if request.user.user_type == 'candidate' and hasattr(request.user, 'candidate'):
            vacancy_args.append('is_applied')
            applied_vacancies = request.user.candidate.applications.filter(vacancy=OuterRef('pk'))

        vacancies = vacancies_page.object_list.annotate(
            is_bookmarked=Case(
                When(Exists(bookmarked_vacancies), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_applied=Case(
                When(Exists(applied_vacancies), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ) if applied_vacancies is not None else Value(False)
        ).values(*vacancy_args)

    else:
        vacancies = vacancies_page.object_list.values(*vacancy_args)

    vacancies_list = list(vacancies)

    pagination_info = {
        'has_next': vacancies_page.has_next(),
        'has_previous': vacancies_page.has_previous(),
        'num_pages': vacancies_page.paginator.num_pages,
        'current_page': vacancies_page.number,
    }

    context = {
        'vacancies': vacancies_list,
        'pagination': pagination_info,
    }

    context['keywords_text'] = tr('Keywords')
    context['apply_now_text'] = tr('Apply Now')
    context['delete_application_text'] = tr('Delete Application')

    return context

def vacancy_with_related_info(objects):
    return objects.select_related('employer').annotate(
        user_id = F('employer__user__id'),
        employer_username = F('employer__user__username'),
        company_name = F('employer__user__first_name'),
        profile_photo_url = Case(
            When(
                employer__user__profile_photo__icontains = 'profile-photos',
                then=Concat(
                    Value(settings.MEDIA_URL),
                    F('employer__user__profile_photo')
                )
            ),
            default=Value(''),
            output_field=CharField()
        )
    )

def fetch_vacancies(request) -> dict:
    # URL parameters are taken for filtering and used for the same filtering on the following pages.
    params = {
        'status': True,
        'delete': False,
        'approval_level': 'PUBLISHED'
    }
    url:str = '' # Creating URL for Pagination

    if salary_range := request.GET.get('salary-range'):
        url += f'&salary-range={salary_range}'
        salary_range_lower = int(salary_range.split(',')[0])
        salary_range_upper = int(salary_range.split(',')[1])

        # lower salary range
        if salary_range_lower:
            params['salary__gte'] = salary_range_lower

        # upper salary range
        if salary_range_upper:
            params['salary__lte'] = salary_range_upper

    if work_experience := request.GET.get('work-experience'):
        url += f'&work-experience={work_experience}'
        params['work_experience_name__in'] = work_experience.split(',')


    if employment_type := request.GET.get('employment-type'):
        url += f'&employment-type={employment_type}'
        params['employment_type_name__in'] = employment_type.split(',')
    
    if sector := request.GET.get('sector'):
        url += f'&sector={sector}'
        params['employer_sector'] = sector

    if department := request.GET.get('department'):
        url += f'&department={department}'
        params['department_name__in'] = department.split(',')

    if work_preference := request.GET.get('work-preference'):
        url += f'&work-preference={work_preference}'
        params['work_preference_name__in'] = work_preference.split(',')

    if career_type := request.GET.get('career-type'):
        url += f'&career-type={career_type}'
        params['career_type_name__in'] = career_type.split(',')

    if date := request.GET.get('date'):
        url += f'&date={date}'
        params['created_date__gte'] = timezone.now() - timedelta(hours=int(date))

    if location := request.GET.get('location'):
        url += f'&location={location}'
        params['location_name'] = location

    if job_family := request.GET.get('job-family'):
        url += f'&job-family={job_family}'
        params['job_title__job_family'] = job_family

    if trending := request.GET.get('trending'):
        url += f'&trending={trending}'
        params['job_title_name'] = trending
    
    # filter settings for view more
    if job_title := request.GET.get('job-title'):
        url += f'&job-title={job_title}'
        params['job_title_name'] = job_title
    
    if company := request.GET.get('company'):
        url += f'&company={company}'
        params['employer__user__first_name'] = company
    # end

    if keyword := request.GET.get('keyword'):
        url += f'&keyword={keyword}'
        try:
            params['keywords__id'] = models.ParameterKeyword.translation().get(name=keyword).id
        except ObjectDoesNotExist: ...

    filtered_vacancies = vacancy_with_related_info(Vacancy.translation_for_filter().filter(**params))

    # Set up Paginator
    paginator = Paginator(filtered_vacancies, 10)
    current_page = request.GET.get('page', 1)
    vacancies = paginator.get_page(current_page)

    # Filter Fields
    locations = models.ParameterLocation.translation().values('id', 'name')
    experiences = models.ParameterWorkExperience.translation().values('id', 'name')
    employments = models.ParameterEmployeeType.translation().values('id', 'name')
    sectors = models.ParameterSector.translation().values('id', 'name')
    departments = models.ParameterDepartment.translation().values('id', 'name')
    work_preferences = models.ParameterWorkPreference.translation().values('id', 'name')
    work_preferences = models.ParameterWorkPreference.translation().values('id', 'name')
    job_family = models.ParameterJobFamily.translation().values('id', 'name')
    date_posted = models.ParameterDatePosted.translation().values('hours', 'name')
    career_types = models.ParameterCareerType.translation().values('id', 'name')

    popular_job_titles = Vacancy.translation().values('job_title_name').annotate(count=Count('job_title_name')).order_by('-count')[:6]

    return {
        'vacancies': vacancies,
        'locations': locations,
        'experiences': experiences,
        'employments': employments,
        'sectors': sectors,
        'departments': departments,
        'work_preferences': work_preferences,
        'url':url,
        'related_vacancies_title': job_title,
        'company': company,
        'popular_job_titles': popular_job_titles,
        'job_family': job_family,
        'date_posted': date_posted,
        'career_types': career_types
    }