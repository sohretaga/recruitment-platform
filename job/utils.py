from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import F, Count, When, Case, Value, CharField
from django.db.models.functions import Concat
from django.conf import settings
from datetime import timedelta

from recruitment_cp import models
from job.models import Vacancy


def get_vacancies_context(request, vacancies) -> dict:
    # Set up Paginator
    paginator = Paginator(vacancies, 10)
    current_page_number = request.POST.get('page', 1)
    vacancies_page = paginator.get_page(current_page_number)

    # Serialize the data
    vacancies_list = list(vacancies_page.object_list.values())
    bookmarks, applications = list(), list()
    keyword_list = list(models.ParameterKeyword.translation().values('id', 'name'))
    keywords = {item['id']: item['name'] for item in keyword_list}

    if request.user.is_authenticated:
        bookmarks = list(request.user.bookmarks.values_list('vacancy__id', flat=True))

    if request.user.is_authenticated and request.user.user_type == 'candidate':
        applications = list(request.user.candidate.applications.values_list('vacancy__id', flat=True))

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
        'applications': applications,
        'keywords': keywords
    }

    return context

def vacancy_with_related_info(objects):
    return objects.select_related('employer').annotate(
        user_id = F('employer__user__id'),
        employer_username = F('employer__user__username'),
        company_name = F('employer__user__first_name'),
        # career_type_name = F('career_type__name'),
        # career_level_name = F('career_level__name'),
        # location_name = F('location__name'),
        # fte_name = F('fte__name'),
        # job_title_name = F('job_title__name'),
        # employment_type_name = F('employment_type__name'),
        # work_experience_name = F('work_experience__name'),
        # work_preference_name = F('work_preference__name'),
        # department_name = F('department__name'),
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
    params = {'status': True, 'delete': False}
    url:str = '' # Creating URL for Pagination

    if salary_range := request.GET.get('salary-range'):
        url += f'&salary-range={salary_range}'
        salary_range_lower = int(salary_range.split(',')[0])
        salary_range_upper = int(salary_range.split(',')[1])

        # lower salary range
        if salary_range_lower:
            params.update({'salary__gte': salary_range_lower})

        # upper salary range
        if salary_range_upper:
            params.update({'salary__lte': salary_range_upper})

    if work_experience := request.GET.get('work-experience'):
        url += f'&work-experience={work_experience}'
        params.update({'work_experience_name__in': work_experience.split(',')})
    
    if employment_type := request.GET.get('employment-type'):
        url += f'&employment-type={employment_type}'
        params.update({'employment_type_name__in': employment_type.split(',')})
    
    if sector := request.GET.get('sector'):
        url += f'&sector={sector}'
        params.update({'employer__sector': sector})

    if department := request.GET.get('department'):
        url += f'&department={department}'
        params.update({'department_name__in': department.split(',')})

    if work_preference := request.GET.get('work-preference'):
        url += f'&work-preference={work_preference}'
        params.update({'work_preference_name__in': work_preference.split(',')})

    if date := request.GET.get('date'):
        url += f'&date={date}'
        params.update({'created_date__gte': timezone.now() - timedelta(hours=int(date))})

    if location := request.GET.get('location'):
        url += f'&location={location}'
        params.update({'location_name': location})

    if job_family := request.GET.get('job-family'):
        url += f'&job-family={job_family}'
        params.update({'job_title__job_family': job_family})

    if trending := request.GET.get('trending'):
        url += f'&trending={trending}'
        params.update({'job_title_name': trending})
    
    # filter settings for view more
    if job_title := request.GET.get('job-title'):
        url += f'&job-title={job_title}'
        params.update({'job_title_name': job_title})
    
    if company := request.GET.get('company'):
        url += f'&company={company}'
        params.update({'employer__user__first_name': company})
    # end

    if keyword := request.GET.get('keyword'):
        url += f'&keyword={keyword}'
        params.update({'keywords__contains': keyword})

    filtered_vacancies = vacancy_with_related_info(Vacancy.translation().filter(**params))

    # Set up Paginator
    paginator = Paginator(filtered_vacancies, 10)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    # Filter Fields
    locations = models.ParameterLocation.translation().values('name')
    experiences = models.ParameterWorkExperience.translation().values('id', 'name')
    employments = models.ParameterEmployeeType.translation().values('id', 'name')
    sectors = models.ParameterSector.translation().values('id', 'name')
    departments = models.ParameterDepartment.translation().values('id', 'name')
    work_preferences = models.ParameterWorkPreference.translation().values('id', 'name')
    work_preferences = models.ParameterWorkPreference.translation().values('id', 'name')
    job_family = models.ParameterJobFamily.translation().values('id', 'name')

    popular_job_titles = Vacancy.translation().values('job_title_name').annotate(count=Count('job_title_name')).order_by('-count')[:6]
    keyword_list = list(models.ParameterKeyword.translation().values('id', 'name'))
    keywords = {item['id']: item['name'] for item in keyword_list}

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
        'keywords': keywords,
        'job_family': job_family
    }