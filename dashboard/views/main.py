from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from job.models import Bookmark


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