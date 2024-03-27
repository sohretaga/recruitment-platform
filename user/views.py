from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from . import forms
from .decorators import logout_required

# Create your views here.

@logout_required
def sign_in(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user=user)
                return redirect('main:main-index')
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
    logout(request)
    return render(request, 'user/sign-out.html')

def reset_password(request):
    if request.POST:
        ...

    return render(request, 'user/reset-password.html')

def profile(request):
    return render(request, 'user/profile.html')


def candidate_list(request):
    return render(request, 'user/candidate-list.html')


def candidate_details(request):
    return render(request, 'user/candidate-details.html')


def company_list(request):
    return render(request, 'user/company-list.html')


def company_details(request):
    return render(request, 'user/company-details.html')