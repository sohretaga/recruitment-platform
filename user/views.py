from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Case, When, CharField, OuterRef, Exists, BooleanField
from django.db.models.functions import Concat
from django.conf import settings

from . import forms
from .models import Gallery, GalleryImage, CandidateBookmark, CandidatePreference
from job.models import Vacancy
from .decorators import logout_required
from user.models import CustomUser, Candidate, Employer, Education, Experience, CandidateBookmark
from job.utils import vacancy_with_related_info
from .utils import manage_user_type_for_details
from dashboard.forms import ManageEmployerAccountForm, ManageCandidateAccountForm
from dashboard.decorators import is_candidate
from recruitment_cp.models import(
        ParameterKeyword,
        ParameterSector,
        ParameterOrganizationType,
        ParameterOrganizationOwnership,
        ParameterNumberOfEmployee,
        ParameterCountry,
        ParameterCompetence,
        ParameterAgeGroup,
        ParameterWorkExperience,
        ParameterEducationLevel,
        ParameterCareerType,
        ParameterLocation,
        ParameterEmployeeType
    )

import os
import json

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


def candidate_list(request):
    params = {}
    url = ''

    if job_family := request.POST.get('job-family'):
        ...
    
    if citizenship := request.GET.get('citizenship'):
        params['citizenship_name__in'] = citizenship.split(',')
        url += f'&citizenship={citizenship}'

    if gender := request.GET.get('gender'):
        params['gender__in'] = gender.split(',')
        url += f'&gender={gender}'

    if age_group := request.GET.get('age-group'):
        params['age_group__in'] = age_group.split(',')
        url += f'&age-group={age_group}'

    if work_experience := request.GET.get('work-experience'):
        params['work_experience_name__in'] = work_experience.split(',')
        url += f'&work-experience={work_experience}'

    if education_level := request.GET.get('education-level'):
        params['education_level_name__in'] = education_level.split(',')
        url += f'&education-level={education_level}'

    candidates = Candidate.translation().filter(**params)
    candidate_count = candidates.count()

    common_filter_args = ('id', 'name')
    citizenships = ParameterCountry.translation().values(*common_filter_args)
    age_groups = ParameterAgeGroup.translation().values(*common_filter_args)
    work_experiences = ParameterWorkExperience.translation().values(*common_filter_args)
    education_levels = ParameterEducationLevel.translation().values(*common_filter_args)

    paginator = Paginator(candidates, 10)
    current_page_number = request.POST.get('page', 1)
    candidates = paginator.get_page(current_page_number)

    context = {
        'candidates': candidates,
        'citizenships': citizenships,
        'age_groups': age_groups,
        'work_experiences': work_experiences,
        'education_levels': education_levels,
        'candidate_count': candidate_count,
        'url': url,
    }

    return render(request, 'user/candidate-list.html', context)

@require_POST
def ajax_filter_candidate(request):
    params = {}

    employer_id = request.user.employer.id \
        if request.user.is_authenticated and \
            request.user.user_type == 'employer' else None

    employer_bookmarked_candidate = CandidateBookmark.objects.filter(
        candidate=OuterRef('pk'),
        employer_id=employer_id
    )

    if job_family := request.POST.get('job-family'):
        ...
    
    if citizenship := request.POST.get('citizenship'):
        params['citizenship_name__in'] = citizenship.split(',')

    if gender := request.POST.get('gender'):
        params['gender__in'] = gender.split(',')

    if age_group := request.POST.get('age-group'):
        params['age_group__in'] = age_group.split(',')

    if work_experience := request.POST.get('work-experience'):
        params['work_experience_name__in'] = work_experience.split(',')

    if education_level := request.POST.get('education-level'):
        params['education_level_name__in'] = education_level.split(',')

    candidates = Candidate.translation().filter(**params)
    candidate_count = candidates.count()

    # Set up Paginator
    paginator = Paginator(candidates, 10)
    current_page_number = request.POST.get('page', 1)
    candidates_page = paginator.get_page(current_page_number)

    # Serialize the data
    candidate_list = list(candidates_page.object_list.annotate(
        username=F('user__username'),
        full_name=Concat(
            F('user__first_name'), Value(' '),
            F('user__last_name')
        ),

        profile_photo=Case(
            When(user__profile_photo__icontains='profile-photos',
                 then=Concat(Value(settings.MEDIA_URL), F('user__profile_photo'))),
                 default=Value(''),
                 output_field=CharField()
        ),

        is_bookmark=Case(
            When(Exists(employer_bookmarked_candidate), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    ).values('id', 'full_name', 'profile_photo', 'is_bookmark', 'username'))

    pagination_info = {
        'has_next': candidates_page.has_next(),
        'has_previous': candidates_page.has_previous(),
        'num_pages': candidates_page.paginator.num_pages,
        'current_page': candidates_page.number,
    }

    context = {
        'candidates': candidate_list,
        'pagination': pagination_info,
        'candidate_count': candidate_count
    }

    return JsonResponse(context, safe=False)


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
    logged_user_context = {}
    candidate = user.candidate
    candidate.views += 1
    candidate.save()

    if username == request.user.username:
        citizenships = ParameterCountry.translation().values('id', 'name')
        competencies = ParameterCompetence.translation().values('id', 'name')
        education_levels = ParameterEducationLevel.translation().values('id', 'name')
        companies = Employer.objects.values('id', 'user__first_name')
        career_types = ParameterCareerType.translation().values('id', 'name')
        locations = ParameterLocation.translation().values('id', 'name')
        types_of_employment = ParameterEmployeeType.translation().values('id', 'name')

        try:
            min_salary = user.candidate.preference.min_salary
            max_salary = user.candidate.preference.max_salary

            if min_salary and max_salary:
                offered_salary = int((int(min_salary) + int(max_salary)) / 2)
            else:
                offered_salary = False

            preference = {
                'companies': user.candidate.preference.companies.values_list('id', flat=True),
                'career_types': user.candidate.preference.career_types.values_list('id', flat=True),
                'locations': user.candidate.preference.locations.values_list('id', flat=True),
                'types_of_employment': user.candidate.preference.types_of_employment.values_list('id', flat=True),
                'offered_salary': offered_salary
            }
        except AttributeError: preference = {}

        logged_user_context = {
            'citizenships': citizenships,
            'competencies': competencies,
            'education_levels': education_levels,
            'companies': companies,
            'career_types': career_types,
            'locations': locations,
            'types_of_employment': types_of_employment,
            'preference': preference
        }
    

    context = {
        'candidate': candidate,
        'educations': user.candidate.educations.all(),
        'experiences': user.candidate.experiences.all(),
        **logged_user_context
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
    vacancies = vacancy_with_related_info(Vacancy.translation().filter(employer=user.employer, status=True, delete=False, approval_level='PUBLISHED')[:5])
    sectors = ParameterSector.translation().values('id', 'name')
    organization_types = ParameterOrganizationType.translation().values('id', 'name')
    organization_ownerships = ParameterOrganizationOwnership.translation().values('id', 'name')
    number_of_employees = ParameterNumberOfEmployee.translation().values('id', 'name')
    locations = ParameterCountry.translation().values('id', 'name')

    keyword_list = ParameterKeyword.translation().values('id', 'name')
    keywords = {item['id']: item['name'] for item in keyword_list}

    try: gallery = user.gallery.images.all()
    except ObjectDoesNotExist: gallery = False

    employer_detail = Employer.translation().get(user=user)

    context = {
        'employer': employer_detail,
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
    education_level_ids = request.POST.getlist('education_level')
    schools = request.POST.getlist('school')
    specialties = request.POST.getlist('speciality')
    start_dates = request.POST.getlist('start_date')
    end_dates = request.POST.getlist('end_date')
    descriptions = request.POST.getlist('description')

    for edu_id, education_level_id, school, speciality, start_date, end_date, description in zip(
        education_ids,
        education_level_ids,
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
        education_level = ParameterEducationLevel.objects.get(id=education_level_id)

        if edu_id:
            education_exists = Education.objects.filter(id=edu_id).exists()
            if education_exists:
                Education.objects.filter(id=edu_id).update(
                    school=school,
                    education_level=education_level,
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
                education_level=education_level,
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
    

@is_candidate
def ajax_manage_candidate_preference(request):
    candidate = request.user.candidate
    companies = json.loads(request.POST.get('companies'))
    locations = json.loads(request.POST.get('locations'))
    career_types = json.loads(request.POST.get('career_types'))
    types_of_employment = json.loads(request.POST.get('types_of_employment'))
    minimum_salary = request.POST.get('minimum_salary')
    maximum_salary = request.POST.get('maximum_salary')

    preference_exists = CandidatePreference.objects.filter(candidate=candidate).exists()
    if preference_exists:
        preference = candidate.preference
    else:
        preference = CandidatePreference.objects.create(candidate=candidate)

    new_companies = Employer.objects.filter(id__in=companies)
    preference.companies.set(new_companies)

    new_career_types = ParameterCareerType.objects.filter(id__in=career_types)
    preference.career_types.set(new_career_types)

    new_locations = ParameterLocation.objects.filter(id__in=locations)
    preference.locations.set(new_locations)

    new_employment_types = ParameterEmployeeType.objects.filter(id__in=types_of_employment)
    preference.types_of_employment.set(new_employment_types)

    if minimum_salary: preference.min_salary = minimum_salary
    if maximum_salary: preference.max_salary = maximum_salary

    preference.save()
    
    return JsonResponse({'status': 200})