from django.shortcuts import render, redirect

from dashboard.forms import CompleteRegisterForm
from user.models import Employer

def complete_register(request):
    if request.POST:
        form = CompleteRegisterForm(request.POST)

        if form.is_valid():
            user = request.user

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            employer = Employer.objects.get(user=user)
            employer.company_name = form.cleaned_data.get('company_name')
            employer.save()
        
        return redirect('main:main-index')

    return render(request, 'dashboard/employer/complete-register.html')