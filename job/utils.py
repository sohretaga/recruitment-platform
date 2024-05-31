from django.core.paginator import Paginator
from recruitment_cp import models

def fetch_vacancies(request) -> dict:
    # URL parameters are taken for filtering and used for the same filtering on the following pages.
    salary_range:str|None = request.GET.get('salary_range')
    work_experiences:str|None = request.GET.get('work_experiences')
    employment_type:str|None = request.GET.get('employment_type')
    params:dict = {}
    url:str = '' # Creating URL for Pagination

    if salary_range:
        url += f'&salary_range={salary_range}'
        salary_range_lower = int(salary_range.split(',')[0])
        salary_range_upper = int(salary_range.split(',')[1])

        # lower salary range
        if salary_range_lower:
            params.update({'salary__gte': salary_range_lower})

        # upper salary range
        if salary_range_upper:
            params.update({'salary__lte': salary_range_upper})

    if work_experiences:
        url += f'&work_experiences={work_experiences}'
        params.update({'work_experience__in': work_experiences.split(',')})
    
    if employment_type:
        url += f'&employment_type={employment_type}'
        params.update({'employment_type__in': employment_type.split(',')})

    filtered_vacancies = models.ParameterVacancy.objects.filter(**params)\
    .values('id', 'no', 'employer__company_name', 'career_type', 'career_level', 'location', 'fte', 'salary_minimum',
            'salary_midpoint', 'salary_maximum', 'salary', 'position_title', 'job_title',
            'employment_type', 'work_experience', 'definition', 'slug', 'created_date')

    # Set up Paginator
    paginator = Paginator(filtered_vacancies, 10)
    current_page = request.GET.get('page')
    vacancies = paginator.get_page(current_page)

    # Filter Fields
    countries = models.ParameterCountry.objects.all().values('name')
    experiences = models.ParameterWorkExperience.objects.all().values('id', 'name')
    employments = models.ParameterEmployeeType.objects.all().values('id', 'name')

    return {
        'vacancies': vacancies,
        'countries': countries,
        'experiences': experiences,
        'employments': employments,
        'url':url
    }