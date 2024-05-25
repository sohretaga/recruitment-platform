from django.core.paginator import Paginator
from recruitment_cp import models

def fetch_vacancies(request) -> dict:

    # Set up Paginator
    paginator = Paginator(models.ParameterVacancy.objects.all(), 10)
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
        'employments': employments
    }