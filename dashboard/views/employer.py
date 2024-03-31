from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from dashboard.forms import CompleteRegisterForm
from user.models import Employer

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