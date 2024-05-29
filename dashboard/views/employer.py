from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

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
            instance.organization = request.user.employer.company_name
            instance.author = request.user
            instance.save()

    selected_language = 'en'
    languages = Language.objects.all()
    job_catalogue = ParameterJobCatalogue.objects.filter(language = selected_language)
    career_types = ParameterCareerType.objects.filter(language=selected_language)
    career_levels = ParameterCareerLevel.objects.filter(language=selected_language)
    locations = ParameterLocation.objects.filter(language=selected_language)
    employment_types = ParameterEmployeeType.objects.filter(language=selected_language)
    ftes = ParameterFTE.objects.filter(language=selected_language)

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
    vacancies = ParameterVacancy.objects.filter(author=request.user).order_by('created_date')

    context = {
        'vacancies': vacancies
    }

    return render(request, 'dashboard/employer/all-vacancies.html', context)