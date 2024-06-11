from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import forms
from .decorators import logout_required
from user.models import CustomUser
from job.models import Bookmark


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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

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
    return render(request, 'user/candidate-list.html')


def candidate_details(request):
    return render(request, 'user/candidate-details.html')


def company_list(request):
    return render(request, 'user/company-list.html')


def company_details(request, username):
    user = get_object_or_404(CustomUser, username=username)
    vacancies = user.employer.vacancies.filter(status=True)[:5]
    bookmarks = Bookmark.objects.filter(user=request.user).values_list('vacancy__id', flat=True)

    context = {
        'employer': user.employer,
        'vacancies': vacancies,
        'bookmarks': bookmarks
    }

    return render(request, 'user/company-details.html', context)