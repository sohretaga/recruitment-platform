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


@login_required
def index(request):
    if request.user.is_superuser:
        return render(request, 'dashboard/index.html')
    
    elif request.user.user_type == 'employer':
        return redirect(reverse('dashboard:all-vacancy'))

    elif request.user.user_type == 'candidate':
        pass

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

    faqs = FAQ.objects.all()

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