from django.shortcuts import redirect, render
from django.urls import reverse

def index(request):
    if request.user.is_superuser:
        return render(request, 'dashboard/index.html')
    
    elif request.user.user_type == 'employer':
        return redirect(reverse('dashboard:post-vacancy'))

    elif request.user.user_type == 'candidate':
        pass

    elif request.user.user_type == 'blogger':
        return redirect(reverse('dashboard:all-blog'))