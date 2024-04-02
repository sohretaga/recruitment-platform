from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from dashboard.decorators import is_employer
from dashboard.forms import CompleteRegisterForm, PostVacancyForm
from user.models import Employer
from recruitment_cp.models import Language, ParameterCareerType, ParameterCareerLevel, ParameterLocation, ParameterEmployeeType, ParameterFTE

@is_employer
@login_required
def complete_register(request):
    if not request.user.is_registration_complete:
        if request.POST:
            form = CompleteRegisterForm(request.POST)

            if form.is_valid():
                user = request.user

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.is_registration_complete = True
                user.save()

                employer = Employer.objects.get(user=user)
                employer.company_name = form.cleaned_data.get('company_name')
                employer.save()
            
            return redirect('main:main-index')

        return render(request, 'dashboard/employer/complete-register.html')
    
    raise Http404


@is_employer
@login_required
def post_vacancy(request):
    if request.POST:
        form = PostVacancyForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.organization = request.user.employer.company_name
            instance.save()

    selected_language = 'en'
    languages = Language.objects.all()
    career_types = ParameterCareerType.objects.filter(language=selected_language)
    career_levels = ParameterCareerLevel.objects.filter(language=selected_language)
    locations = ParameterLocation.objects.filter(language=selected_language)
    employment_types = ParameterEmployeeType.objects.filter(language=selected_language)
    ftes = ParameterFTE.objects.filter(language=selected_language)

    context = {
        'languages': languages,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes
    }
    
    return render(request, 'dashboard/employer/post-vacancy.html', context)