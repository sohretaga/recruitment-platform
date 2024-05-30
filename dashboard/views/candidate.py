from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from dashboard.decorators import is_candidate
from dashboard.forms import CompleteCandidateRegisterForm

@is_candidate
@login_required
def complete_register(request):
    if not request.user.is_registration_complete:
        if request.POST:
            form = CompleteCandidateRegisterForm(request.POST)

            if form.is_valid():
                user = request.user

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.is_registration_complete = True
                user.save()

            return redirect('main:main-index')

        return render(request, 'dashboard/complete-register.html')

    raise Http404

@is_candidate
@login_required
def your_applies(request):
    return render(request,  'dashboard/candidate/your-applies.html')