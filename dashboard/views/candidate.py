from django.shortcuts import render, redirect
from django.urls import reverse

from dashboard.decorators import is_candidate
from dashboard.forms import ManageCandidateAccountForm
from recruitment_cp.models import ParameterCountry

@is_candidate
def your_applies(request):
    return render(request, 'dashboard/candidate/your-applies.html')

@is_candidate
def manage_account(request):
    if request.POST:
        user = request.user
        form = ManageCandidateAccountForm(request.POST, request.FILES, instance=user.candidate)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            profile_photo = form.cleaned_data.get('profile_photo')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            if profile_photo:
                user.profile_photo = profile_photo

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_registration_complete = True
            user.save()

            return redirect(reverse('dashboard:your-applies'))
    
    citizenship = ParameterCountry.objects.all()

    context = {
        'citizenship': citizenship
    }

    return render(request, 'dashboard/candidate/manage-account.html', context)