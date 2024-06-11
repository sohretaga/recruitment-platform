from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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