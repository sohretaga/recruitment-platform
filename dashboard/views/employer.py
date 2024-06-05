from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

from django.http import Http404, JsonResponse
from django.core.paginator import Paginator

from dashboard.decorators import is_employer
from dashboard.forms import CompleteEmployerRegisterForm, PostVacancyForm
from recruitment_cp.models import (Language,
                                   ParameterCareerType,
                                   ParameterCareerLevel,
                                   ParameterLocation,
                                   ParameterEmployeeType,
                                   ParameterFTE,
                                   ParameterJobCatalogue,
                                   ParameterWorkPreference,
                                   ParameterDepartment
                                )

@is_employer
@login_required
def complete_register(request):
    if not request.user.is_registration_complete:
        if request.POST:
            form = CompleteEmployerRegisterForm(request.POST)

            if form.is_valid():
                user = request.user

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.is_registration_complete = True
                user.employer.company_name = form.cleaned_data.get('company_name')
                user.save()
            
            return redirect('main:main-index')

        return render(request, 'dashboard/complete-register.html')
    
    raise Http404


@is_employer
@login_required
def post_vacancy(request):
    if request.POST:
        form = PostVacancyForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.employer = request.user.employer
            instance.save()
            return redirect(reverse('dashboard:all-vacancy'))

    selected_language = 'en'
    languages = Language.objects.all().values('code', 'name')
    job_catalogue = ParameterJobCatalogue.objects.filter(language = selected_language).values('name')
    career_types = ParameterCareerType.objects.filter(language=selected_language).values('name')
    career_levels = ParameterCareerLevel.objects.filter(language=selected_language).values('name')
    locations = ParameterLocation.objects.filter(language=selected_language).values('name')
    employment_types = ParameterEmployeeType.objects.filter(language=selected_language).values('name')
    ftes = ParameterFTE.objects.filter(language=selected_language).values('name')
    work_preferences = ParameterWorkPreference.objects.filter(language=selected_language).values('name')
    departments = ParameterDepartment.objects.filter(language=selected_language).values('name')

    context = {
        'languages': languages,
        'job_catalogues': job_catalogue,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes,
        'work_preferences': work_preferences,
        'departments': departments
    }
    
    return render(request, 'dashboard/employer/post-vacancy.html', context)


@is_employer
@login_required
def all_vacancy(request):
    return render(request, 'dashboard/employer/all-vacancies.html')

def ajax_all_vacancy(request):
    start:str = int(request.GET.get('start', 0))
    length:str = int(request.GET.get('length', 10))
    search_value:str = request.GET.get('search[value]', '')

    vacancies = request.user.employer.vacancies.all()

    if search_value:
        vacancies = vacancies.filter(position_title__icontains=search_value)

    paginator = Paginator(vacancies, length)
    page_number = (start // length) + 1
    page_vacancies = paginator.get_page(page_number)

    data = []
    for obj in page_vacancies:
        data.append([
            obj.position_title,
            obj.job_title,
            obj.career_type,
            obj.career_level,
            obj.salary_minimum,
            obj.salary_midpoint,
            obj.salary_maximum,
            obj.salary,
            obj.views,
            obj.id,
            obj.slug,
        ])

    response = {
        "draw": request.GET.get('draw', 1),
        "recordsTotal": paginator.count,
        "recordsFiltered": paginator.count,
        "data": data,
    }

    return JsonResponse(response)


@is_employer
@login_required
def edit_vacancy(request, id):
    vacancy = get_object_or_404(request.user.employer.vacancies, id=id)

    selected_language = 'en'
    languages = Language.objects.all().values('code', 'name')
    job_catalogue = ParameterJobCatalogue.objects.filter(language = selected_language).values('name')
    career_types = ParameterCareerType.objects.filter(language=selected_language).values('name')
    career_levels = ParameterCareerLevel.objects.filter(language=selected_language).values('name')
    locations = ParameterLocation.objects.filter(language=selected_language).values('name')
    employment_types = ParameterEmployeeType.objects.filter(language=selected_language).values('name')
    ftes = ParameterFTE.objects.filter(language=selected_language).values('name')
    work_preferences = ParameterWorkPreference.objects.filter(language=selected_language).values('name')
    departments = ParameterDepartment.objects.filter(language=selected_language).values('name')

    if request.POST:
        form = PostVacancyForm(request.POST, instance=vacancy)

        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:all-vacancy'))

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
        'departments': departments
    }

    return render(request, 'dashboard/employer/post-vacancy.html', context)