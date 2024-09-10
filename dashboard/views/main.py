from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from job.models import Bookmark
from main.models import FAQ
from recruitment_cp.models import ParameterFAQ
from dashboard.forms import ManageFaqForm
from dashboard.decorators import is_superuser

from recruitment_cp.models import (
    Language,
    ParameterCareerType,
    ParameterCareerLevel,
    ParameterLocation,
    ParameterEmployeeType,
    ParameterFTE,
    ParameterJobCatalogue,
    ParameterWorkPreference,
    ParameterDepartment,
    ParameterKeyword,
)


@login_required
def index(request):
    if request.user.is_superuser:
        return render(request, 'dashboard/index.html')
    
    elif request.user.user_type == 'employer':
        return redirect(reverse('dashboard:all-vacancy'))

    elif request.user.user_type == 'candidate':
        return redirect(reverse('dashboard:applications'))

    elif request.user.user_type == 'blogger':
        return redirect(reverse('dashboard:all-blog'))
    
@login_required
def bookmarks(request):
    bookmarks = request.user.bookmarks.all()

    context = {
        'bookmarks': bookmarks
    }

    return render(request, 'dashboard/bookmarks.html', context)

@require_POST
def ajax_delete_bookmark(request):
    bookmark_id = request.POST.get('bookmark_id')
    bookmark = Bookmark.objects.filter(id=bookmark_id)

    if request.user == bookmark.first().user:
        bookmark.delete()

    return JsonResponse({'status':200})

@is_superuser
def faqs(request):
    if request.POST:
        ...

    faqs = FAQ.translation().values('id', 'category_name', 'question').order_by('category_name')

    context = {
        'faqs':faqs
    }

    return render(request, 'dashboard/faqs.html', context)

@is_superuser
def add_faq(request):
    if request.POST:
        form = ManageFaqForm(request.POST)

        if form.is_valid:
            form.save()
            return redirect(reverse('dashboard:faqs'))

    categories = ParameterFAQ.objects.all()

    context = {
        'categories': categories
    }
    
    return render(request, 'dashboard/manage-faq.html', context)

@is_superuser
def edit_faq(request, id):
    faq = FAQ.objects.get(id=id)

    if request.POST:
        form = ManageFaqForm(request.POST, instance=faq)

        if form.is_valid:
            form.save()

            return redirect(reverse('dashboard:faqs'))
    
    categories = ParameterFAQ.objects.all()

    context = {
        'categories': categories,
        'faq': faq
    }

    return render(request, 'dashboard/manage-faq.html', context)


@require_POST
def ajax_delete_faq(request):
    faq_id = request.POST.get('faq_id')
    faq = FAQ.objects.filter(id=faq_id)

    if request.user.is_superuser:
        faq.delete()

    return JsonResponse({'status':200})

def get_vacancy_context() -> dict:
    languages = Language.objects.values('code', 'name')
    job_catalogue = ParameterJobCatalogue.translation().values('id', 'name').order_by('name')
    career_types = ParameterCareerType.translation().values('id', 'name')
    career_levels = ParameterCareerLevel.translation().values('id', 'name')
    locations = ParameterLocation.translation().values('id', 'name')
    employment_types = ParameterEmployeeType.translation().values('id', 'name')
    ftes = ParameterFTE.translation().values('id', 'name')
    work_preferences = ParameterWorkPreference.translation().values('id', 'name')
    departments = ParameterDepartment.translation().values('id', 'name')
    keywords = ParameterKeyword.translation().values('id', 'name')

    context = {
        'languages': languages,
        'job_catalogues': job_catalogue,
        'career_types': career_types,
        'career_levels': career_levels,
        'locations': locations,
        'employment_types': employment_types,
        'ftes': ftes,
        'work_preferences': work_preferences,
        'departments': departments,
        'keywords': keywords
    }

    return context