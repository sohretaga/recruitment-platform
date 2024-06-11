from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone

from recruitment_cp import models
from job.models import Vacancy, Bookmark

def fetch_vacancies(request) -> dict:
    # URL parameters are taken for filtering and used for the same filtering on the following pages.
    salary_range:str|None = request.GET.get('salary-range')
    work_experience:str|None = request.GET.get('work-experience')
    employment_type:str|None = request.GET.get('employment-type')
    sector:str|None = request.GET.get('sector')
    department:str|None = request.GET.get('department')
    work_preference:str|None = request.GET.get('work-preference')
    date:str|None = request.GET.get('date')
    job_title:str|None = request.GET.get('job-title')
    company:str|None = request.GET.get('company')
    params = {'status': True}
    url:str = '' # Creating URL for Pagination

    if salary_range:
        url += f'&salary-range={salary_range}'
        salary_range_lower = int(salary_range.split(',')[0])
        salary_range_upper = int(salary_range.split(',')[1])

        # lower salary range
        if salary_range_lower:
            params.update({'salary__gte': salary_range_lower})

        # upper salary range
        if salary_range_upper:
            params.update({'salary__lte': salary_range_upper})

    if work_experience:
        url += f'&work-experience={work_experience}'
        params.update({'work_experience__in': work_experience.split(',')})
    
    if employment_type:
        url += f'&employment-type={employment_type}'
        params.update({'employment_type__in': employment_type.split(',')})
    
    if sector:
        url += f'&sector={sector}'
        params.update({'employer__company__sector': sector})

    if department:
        url += f'&department={department}'
        params.update({'department__in': department.split(',')})

    if work_preference:
        url += f'&work-preference={work_preference}'
        params.update({'work_preference__in': work_preference.split(',')})

    if date:
        url += f'&date={date}'
        params.update({'created_date__gte': timezone.now() - timedelta(hours=int(date))})
    
    # filter settings for view more
    if job_title:
        url += f'&job-title={job_title}'
        params.update({'job_title': job_title})
    
    if company:
        url += f'&company={company}'
        params.update({'employer__company_name': company})

    filtered_vacancies = Vacancy.objects.filter(**params)

    # Set up Paginator
    paginator = Paginator(filtered_vacancies, 10)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    # Filter Fields
    countries = models.ParameterCountry.objects.values('name')
    experiences = models.ParameterWorkExperience.objects.values('id', 'name')
    employments = models.ParameterEmployeeType.objects.values('id', 'name')
    sectors = models.ParameterSector.objects.values('id', 'name')
    departments = models.ParameterDepartment.objects.values('id', 'name')
    work_preferences = models.ParameterWorkPreference.objects.values('id', 'name')

    bookmarks = Bookmark.objects.filter(user=request.user).values_list('vacancy__id', flat=True)

    return {
        'vacancies': vacancies,
        'countries': countries,
        'experiences': experiences,
        'employments': employments,
        'sectors': sectors,
        'departments': departments,
        'work_preferences': work_preferences,
        'url':url,
        'related_vacancies_title': job_title,
        'company': company,
        'bookmarks': bookmarks
    }