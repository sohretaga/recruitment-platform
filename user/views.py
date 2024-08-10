from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from .models import Gallery, GalleryImage, CandidateBookmark
from job.models import Vacancy
from .decorators import logout_required
from user.models import CustomUser, Candidate, Employer, Education, Experience
from job.utils import vacancy_with_related_info
from .utils import manage_user_type_for_details
from dashboard.forms import ManageEmployerAccountForm, ManageCandidateAccountForm
from recruitment_cp.models import(
        ParameterKeyword,
        ParameterSector,
        ParameterOrganizationType,
        ParameterOrganizationOwnership,
        ParameterNumberOfEmployee,
        ParameterCountry,
        ParameterCompetence
    )

import os

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
    if request.POST:
        user = request.user
        form = ManageCandidateAccountForm(request.POST, request.FILES, instance=user.candidate)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            profile_photo = form.cleaned_data.get('profile_photo')
            phone_number = form.cleaned_data.get('phone_number')
            about = form.cleaned_data.get('about')
            address = form.cleaned_data.get('address')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            languages = form.cleaned_data.get('languages')
            instance = form.save(commit=False)
            
            if languages:
                instance.languages = languages.split(',')

            instance.save()

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
        
    params = manage_user_type_for_details(request, username, user_type='candidate')

    user = get_object_or_404(CustomUser, **params)
    citizenships = ParameterCountry.objects.values('id', 'name')
    competencies = ParameterCompetence.objects.values('id', 'name')

    context = {
        'candidate': user.candidate,
        'citizenships': citizenships,
        'competencies': competencies,
        'educations': user.candidate.educations.all(),
        'experiences': user.candidate.experiences.all()
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
    if request.POST:
        user = request.user
        form = ManageEmployerAccountForm(request.POST, request.FILES, instance=user.employer)

        if form.is_valid():
            email = form.cleaned_data.get('primary_email')
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

            return redirect(reverse('user:company', args=[user.username]))
        
    params = manage_user_type_for_details(request, username, user_type='employer')

    user = get_object_or_404(CustomUser, **params)
    vacancies = vacancy_with_related_info(Vacancy.translation().filter(employer=user.employer, status=True, delete=False)[:5])
    sectors = ParameterSector.translation().values('id', 'name')
    organization_types = ParameterOrganizationType.translation().values('id', 'name')
    organization_ownerships = ParameterOrganizationOwnership.translation().values('id', 'name')
    number_of_employees = ParameterNumberOfEmployee.translation().values('id', 'name')
    locations = ParameterCountry.translation().values('id', 'name')

    keyword_list = ParameterKeyword.translation().values('id', 'name')
    keywords = {item['id']: item['name'] for item in keyword_list}

    try: gallery = user.gallery.images.all()
    except ObjectDoesNotExist: gallery = False

    context = {
        'employer': user.employer,
        'vacancies': vacancies,
        'keywords': keywords,
        'sectors': sectors,
        'organization_types': organization_types,
        'organization_ownerships': organization_ownerships,
        'number_of_employees': number_of_employees,
        'locations': locations,
        'gallery': gallery
    }

    return render(request, 'user/company-details.html', context)

@login_required
@require_POST
def gallery_upload(request):
    gallery = Gallery.objects.get_or_create(user=request.user)[0]

    image_ids = request.POST.getlist('image-id', [])
    titles = request.POST.getlist('title', [])
    descriptions = request.POST.getlist('description', [])

    for image_id, title, description in zip(image_ids, titles, descriptions):

        try: image_exists = GalleryImage.objects.filter(id=image_id).exists()
        except ValueError: image_exists = False

        if image_exists:
            GalleryImage.objects.filter(id=image_id).update(
                title=title,
                description=description
            )

        else:
            image = request.FILES.get(f'image-{image_id}')

            if image:
                GalleryImage.objects.create(
                    gallery=gallery,
                    image=image,
                    title=title,
                    description=description
                )

    return redirect(reverse('user:company', args=[request.user]))

@login_required
@require_POST
def delete_gallery_image(request):
    image_id = request.POST.get('image_id', 0)
    image_exists = GalleryImage.objects.filter(id=image_id, gallery__user=request.user).exists()

    if image_exists:
        GalleryImage.objects.filter(id=image_id, gallery__user=request.user).delete()

    return JsonResponse({'status': 200})

@login_required
@require_POST
def manage_education(request):
    education_ids = request.POST.getlist('education_id')
    schools = request.POST.getlist('school')
    specialties = request.POST.getlist('speciality')
    start_dates = request.POST.getlist('start_date')
    end_dates = request.POST.getlist('end_date')
    descriptions = request.POST.getlist('description')

    for edu_id, school, speciality, start_date, end_date, description in zip(
        education_ids,
        schools,
        specialties,
        start_dates,
        end_dates,
        descriptions
    ):
        start_date = start_date.split(',')
        start_date_month = start_date[0]
        start_date_year = start_date[1]

        end_date = end_date.split(',')
        end_date_month = end_date[0]
        end_date_year = end_date[1]

        if edu_id:
            education_exists = Education.objects.filter(id=edu_id).exists()
            if education_exists:
                Education.objects.filter(id=edu_id).update(
                    school=school,
                    speciality=speciality,
                    start_date_month=start_date_month,
                    start_date_year=start_date_year,
                    end_date_month=end_date_month,
                    end_date_year=end_date_year,
                    description=description
                )
        else:
            Education.objects.create(
                candidate=request.user.candidate,
                school=school,
                speciality=speciality,
                start_date_month=start_date_month,
                start_date_year=start_date_year,
                end_date_month=end_date_month,
                end_date_year=end_date_year,
                description=description
            )        
    
    return redirect(reverse('user:candidate', args=[request.user]))
    

@login_required
@require_POST
def delete_education(request):
    education_id = request.POST.get('education_id', 0)
    education_exists = Education.objects.filter(id=education_id, candidate=request.user.candidate).exists()

    if education_exists:
        Education.objects.filter(id=education_id, candidate=request.user.candidate).delete()

    return JsonResponse({'status': 200})


@login_required
@require_POST
def manage_experience(request):
    experience_ids = request.POST.getlist('experience_id')
    company_names = request.POST.getlist('company_name')
    titles = request.POST.getlist('title')
    start_dates = request.POST.getlist('start_date')
    end_dates = request.POST.getlist('end_date')
    descriptions = request.POST.getlist('description')
    present_ids = request.POST.getlist('present_id')

    for exp_id, company_name, title, start_date, end_date, description, present_id in zip(
        experience_ids,
        company_names,
        titles,
        start_dates,
        end_dates,
        descriptions,
        present_ids
    ):
        present = request.POST.get(f'present-{present_id}') == 'on'
        
        start_date = start_date.split(',')
        start_date_month = start_date[0]
        start_date_year = start_date[1]

        end_date_month = None
        end_date_year = None

        if end_date and not present:
            end_date = end_date.split(',')
            end_date_month = end_date[0]
            end_date_year = end_date[1]

        if exp_id:
            experience_exists = Experience.objects.filter(id=exp_id).exists()
            if experience_exists:
                Experience.objects.filter(id=exp_id).update(
                    company_name=company_name,
                    title=title,
                    start_date_month=start_date_month,
                    start_date_year=start_date_year,
                    end_date_month=end_date_month,
                    end_date_year=end_date_year,
                    description=description,
                    present=present
                )
        else:
            Experience.objects.create(
                candidate=request.user.candidate,
                company_name=company_name,
                title=title,
                start_date_month=start_date_month,
                start_date_year=start_date_year,
                end_date_month=end_date_month,
                end_date_year=end_date_year,
                description=description,
                present=present
            )  
    
    return redirect(reverse('user:candidate', args=[request.user]))
    

@login_required
@require_POST
def delete_experience(request):
    experience_id = request.POST.get('experience_id', 0)
    experience_exists = Experience.objects.filter(id=experience_id, candidate=request.user.candidate).exists()

    if experience_exists:
        Experience.objects.filter(id=experience_id, candidate=request.user.candidate).delete()

    return JsonResponse({'status': 200})

@login_required
@require_POST
def delete_pfofile_image(request):
    user = request.user
    image_id = request.POST.get('image_id')

    if image_id == 'profile-img':
        if os.path.isfile(user.profile_photo.path):
            os.remove(user.profile_photo.path)

        user.profile_photo = ''
        user.save()
    else:
        if os.path.isfile(user.employer.background_image.path):
            os.remove(user.employer.background_image.path)

        user.employer.background_image = ''
        user.employer.save()

    return JsonResponse({'status': 200})

@login_required
@require_POST
def ajax_candidate_bookmarks(request):
    candidate_id = request.POST.get('candidate')
    candidate = Candidate.objects.get(id=candidate_id)
    params = {
        'employer': request.user.employer,
        'candidate': candidate
    }

    candidate_bookmark_exists = CandidateBookmark.objects.filter(**params).exists()

    if candidate_bookmark_exists:
        CandidateBookmark.objects.filter(**params).delete()
        return JsonResponse({'status': 'success', 'message': 'Bookmark removed'})
    else:
        CandidateBookmark.objects.create(**params)
        return JsonResponse({'status': 'success', 'message': 'Bookmark added'})