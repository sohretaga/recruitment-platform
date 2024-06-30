from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import F
from django.http import JsonResponse

from dashboard.decorators import is_candidate
from dashboard.forms import ManageCandidateAccountForm
from recruitment_cp.models import ParameterCountry
from job.models import Apply

@is_candidate
def your_applies(request):
    applications = request.user.candidate.applications.select_related('vacancy', 'candidate').annotate(
        company_name=F('candidate__user__first_name'),
        position_title=F('vacancy__position_title'),
        job_title=F('vacancy__job_title__name'),
        career_level=F('vacancy__career_level__name'),
        slug=F('vacancy__slug'),
    ).values('id', 'company_name', 'position_title', 'job_title', 'career_level', 'slug').order_by('-created_date')

    context = {
        'applications': applications
    }

    return render(request, 'dashboard/candidate/your-applies.html', context)

@is_candidate
def manage_account(request):
    if request.POST:
        user = request.user
        form = ManageCandidateAccountForm(request.POST, request.FILES, instance=user.candidate)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            profile_photo = form.cleaned_data.get('profile_photo')
            phone_number = form.cleaned_data.get('phone_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            if profile_photo:
                user.profile_photo = profile_photo

            user.email = email
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.is_registration_complete = True
            user.save()

            return redirect(reverse('dashboard:applications'))
    
    citizenships = ParameterCountry.objects.all()

    context = {
        'citizenships': citizenships
    }

    return render(request, 'dashboard/candidate/manage-account.html', context)

@require_POST
def ajax_delete_apply(request):
    apply_id = request.POST.get('apply_id')
    apply = Apply.objects.filter(id=apply_id)

    if request.user == apply.first().candidate.user:
        apply.delete()

    return JsonResponse({'status': 200})