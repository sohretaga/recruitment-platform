from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from . import forms
from .decorators import logout_required
from user.models import CustomUser, Candidate, Employer
from job.utils import vacancy_with_related_info
from recruitment_cp.models import ParameterKeyword, ParameterSector, ParameterOrganizationType, ParameterOrganizationOwnership, ParameterNumberOfEmployee, ParameterCountry
from dashboard.forms import ManageEmployerAccountForm, ManageCandidateAccountForm


@logout_required
def sign_in(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user=user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Username or password is wrong!')

    return render(request, 'user/sign-in.html')

@logout_required
def sign_up(request):
    if request.POST:
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user=user)
                return redirect('main:main-index')

        else:
            user_type = form.cleaned_data.get('user_type')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            terms = form.cleaned_data.get('terms')

            context = {
                'user_type': user_type,
                'username': username,
                'email': email,
                'terms': terms
            }

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return render(request, 'user/sign-up.html', context)

    return render(request, 'user/sign-up.html')

def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'user/sign-out.html')

@logout_required
def reset_password(request):
    if request.POST:
        ...

    return render(request, 'user/reset-password.html')

@login_required
def profile(request):
    return render(request, 'user/profile.html')


def candidate_list(request):
    candidates = Candidate.objects.all()

    context = {
        'candidates': candidates
    }

    return render(request, 'user/candidate-list.html', context)


def candidate_details(request, username):
   # If the logged-in user is a superuser
    if request.user.is_superuser:
        # Superusers can act as both "employer" and "candidate"
        # Therefore, only the username information is sufficient
        params = {
            'username': username,
        }
    else:
        # Non-superuser users can only act as "candidate"
        # Therefore, both username and user_type information are required
        params = {
            'username': username,
            'user_type': 'candidate'
        }

    user = get_object_or_404(CustomUser, **params)

    if request.POST:
        user = request.user
        form = ManageCandidateAccountForm(request.POST, request.FILES, instance=user.candidate)

        print(form.errors)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            profile_photo = form.cleaned_data.get('profile_photo')
            phone_number = form.cleaned_data.get('phone_number')
            about = form.cleaned_data.get('about')
            address = form.cleaned_data.get('address')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            if profile_photo:
                user.profile_photo = profile_photo

            user.email = email
            user.phone_number = phone_number
            user.about = about
            user.address = address
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect(reverse('user:candidate', args=[user.username]))
    
    citizenships = ParameterCountry.objects.values('id', 'name')

    context = {
        'candidate': user.candidate,
        'citizenships': citizenships
    }

    return render(request, 'user/candidate-details.html', context)


def company_list(request):
    companies = Employer.objects.all().order_by('user__first_name')

    paginator = Paginator(companies, 30)
    current_page = request.GET.get('page')
    companies = paginator.get_page(current_page)

    context = {
        'companies': companies
    }

    return render(request, 'user/company-list.html', context)


def company_details(request, username):
    # If the logged-in user is a superuser
    if request.user.is_superuser:
        # Superusers can act as both "employer" and "candidate"
        # Therefore, only the username information is sufficient
        params = {
            'username': username,
        }
    else:
        # Non-superuser users can only act as "candidate"
        # Therefore, both username and user_type information are required
        params = {
            'username': username,
            'user_type': 'candidate'
        }

    user = get_object_or_404(CustomUser, **params)
    vacancies = vacancy_with_related_info(user.employer.vacancies.filter(status=True)[:5])
    keywords = ParameterKeyword.objects.all()
    sectors = ParameterSector.objects.all().values('id', 'name')
    organization_types = ParameterOrganizationType.objects.all().values('id', 'name')
    organization_ownerships = ParameterOrganizationOwnership.objects.all().values('id', 'name')
    number_of_employees = ParameterNumberOfEmployee.objects.all().values('id', 'name')

    if request.POST:
        user = request.user
        form = ManageEmployerAccountForm(request.POST, request.FILES, instance=user.employer)

        if form.is_valid():
            email = form.cleaned_data.get('primary_email')
            profile_photo = form.cleaned_data.get('profile_photo')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            if profile_photo:
                user.profile_photo = profile_photo

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect(reverse('user:company', args=[user.username]))
    context = {
        'employer': user.employer,
        'vacancies': vacancies,
        'keywords': keywords,
        'sectors': sectors,
        'organization_types': organization_types,
        'organization_ownerships': organization_ownerships,
        'number_of_employees': number_of_employees
    }

    return render(request, 'user/company-details.html', context)