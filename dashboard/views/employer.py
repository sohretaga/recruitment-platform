from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse

from dashboard.decorators import is_employer
from dashboard.forms import CompleteEmployerRegisterForm, PostVacancyForm
from recruitment_cp.models import (Language,
                                   ParameterCareerType,
                                   ParameterCareerLevel,
                                   ParameterLocation,
                                   ParameterEmployeeType,
                                   ParameterFTE,
                                   ParameterJobCatalogue,
                                   ParameterVacancy
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
            instance.author = request.user
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

    context = {
        'languages': languages,
        'job_catalogues': job_catalogue,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes
    }
    
    return render(request, 'dashboard/employer/post-vacancy.html', context)


@is_employer
@login_required
def all_vacancy(request):
    vacancies = ParameterVacancy.objects.filter(author=request.user).order_by('created_date')\
    .values('id', 'position_title', 'job_title', 'career_type', 'career_level', 'salary_minimum', 'salary_midpoint', 'salary_maximum', 'salary', 'views')

    context = {
        'vacancies': vacancies
    }

    return render(request, 'dashboard/employer/all-vacancies.html', context)

@is_employer
@login_required
def edit_vacancy(request, id):
    vacancy = get_object_or_404(ParameterVacancy, id=id)

    selected_language = 'en'
    languages = Language.objects.all().values('code', 'name')
    job_catalogue = ParameterJobCatalogue.objects.filter(language = selected_language).values('name')
    career_types = ParameterCareerType.objects.filter(language=selected_language).values('name')
    career_levels = ParameterCareerLevel.objects.filter(language=selected_language).values('name')
    locations = ParameterLocation.objects.filter(language=selected_language).values('name')
    employment_types = ParameterEmployeeType.objects.filter(language=selected_language).values('name')
    ftes = ParameterFTE.objects.filter(language=selected_language).values('name')

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
        'ftes': ftes
    }

    return render(request, 'dashboard/employer/post-vacancy.html', context)