from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from dashboard.decorators import is_employer
from dashboard.forms import PostVacancyForm, ManageEmployerAccountForm
from job.models import Vacancy
from job.utils import vacancy_with_related_info
from recruitment_cp.models import (
    Language,
    ParameterCareerType,
    ParameterCareerLevel,
    ParameterLocation,
    ParameterEmployeeType,
    ParameterFTE,
    ParameterJobCatalogue,
    ParameterWorkPreference,
    ParameterDepartment,
    ParameterSector,
    ParameterOrganizationType,
    ParameterOrganizationOwnership,
    ParameterNumberOfEmployee,
    ParameterKeyword
)


@is_employer
def post_vacancy(request):
    if request.POST:
        form = PostVacancyForm(request.POST)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.employer = request.user.employer
            instance.save()
            return redirect(reverse('dashboard:all-vacancy'))

    languages = Language.objects.values('code', 'name')
    job_catalogue = ParameterJobCatalogue.translation().values('id', 'name')
    career_types = ParameterCareerType.translation().values('id', 'name')
    career_levels = ParameterCareerLevel.translation().values('id', 'name')
    locations = ParameterLocation.translation().values('id', 'name')
    employment_types = ParameterEmployeeType.translation().values('id', 'name')
    ftes = ParameterFTE.translation().values('id', 'name')
    work_preferences = ParameterWorkPreference.translation().values('id', 'name')
    departments = ParameterDepartment.translation().values('id', 'name')
    keywords = ParameterKeyword.translation().values('id', 'name')

    context = {
        'languages': languages,
        'job_catalogues': job_catalogue,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes,
        'work_preferences': work_preferences,
        'departments': departments,
        'keywords': keywords
    }
    
    return render(request, 'dashboard/employer/post-vacancy.html', context)


@is_employer
def all_vacancy(request):
    return render(request, 'dashboard/employer/all-vacancies.html')

def ajax_all_vacancy(request):
    start:str = int(request.GET.get('start', 0))
    length:str = int(request.GET.get('length', 10))
    search_value:str = request.GET.get('search[value]', '')

    vacancies = vacancy_with_related_info(Vacancy.translation().filter(employer=request.user.employer, delete=False))

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
        ])

    response = {
        "draw": request.GET.get('draw', 1),
        "recordsTotal": paginator.count,
        "recordsFiltered": paginator.count,
        "data": data,
    }

    return JsonResponse(response)


@is_employer
def edit_vacancy(request, id):
    vacancy = get_object_or_404(request.user.employer.vacancies, id=id)
    if request.POST:
        form = PostVacancyForm(request.POST, instance=vacancy)

        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            instance = form.save(commit=False)
            instance.keywords = keywords
            instance.save()
            return redirect(reverse('dashboard:all-vacancy'))
        
    languages = Language.objects.values('code', 'name')
    job_catalogue = ParameterJobCatalogue.translation().values('id', 'name')
    career_types = ParameterCareerType.translation().values('id', 'name')
    career_levels = ParameterCareerLevel.translation().values('id', 'name')
    locations = ParameterLocation.translation().values('id', 'name')
    employment_types = ParameterEmployeeType.translation().values('id', 'name')
    ftes = ParameterFTE.translation().values('id', 'name')
    work_preferences = ParameterWorkPreference.translation().values('id', 'name')
    departments = ParameterDepartment.translation().values('id', 'name')
    keywords = ParameterKeyword.translation().values('id', 'name')

    context = {
        'vacancy': vacancy,
        'languages': languages,
        'job_catalogues': job_catalogue,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes,
        'work_preferences': work_preferences,
        'departments': departments,
        'keywords': keywords
    }

    return render(request, 'dashboard/employer/post-vacancy.html', context)

@is_employer
def manage_account(request):
    if request.POST:
        user = request.user
        form = ManageEmployerAccountForm(request.POST, request.FILES, instance=user.employer)

        if form.is_valid():
            email = form.cleaned_data.get('primary_email')
            profile_photo = form.cleaned_data.get('profile_photo')
            phone_number = form.cleaned_data.get('phone_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            if profile_photo:
                user.profile_photo = profile_photo

            user.email = email
            user.first_name = first_name
            user.phone_number = phone_number
            user.last_name = last_name
            user.is_registration_complete = True
            user.save()

            return redirect(reverse('dashboard:all-vacancy'))

    sectors = ParameterSector.translation().values('id', 'name')
    organization_types = ParameterOrganizationType.translation().values('id', 'name')
    organization_ownerships = ParameterOrganizationOwnership.translation().values('id', 'name')
    number_of_employees = ParameterNumberOfEmployee.translation().values('id', 'name')

    context = {
        'sectors': sectors,
        'organization_types': organization_types,
        'organization_ownerships': organization_ownerships,
        'number_of_employees': number_of_employees
    }

    return render(request, 'dashboard/employer/manage-account.html', context)

@require_POST
def ajax_delete_vacancy(request):
    vacnacy_id = request.POST.get('vacancy_id')
    vacancy = Vacancy.objects.filter(id=vacnacy_id)

    if request.user == vacancy.first().employer.user:
        vacancy.update(delete=True)

    return JsonResponse({'status': 200})