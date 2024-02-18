from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from . import forms

# Create your views here.

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

    return render(request, 'user/sign-in.html')

def sign_up(request):
    if request.POST:
        ...

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