from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from dashboard.decorators import is_blogger
from dashboard.forms import PostBlogForm

@is_blogger
@login_required
def post_blog(request):
    if request.POST:
        form = PostBlogForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

    return render(request, 'dashboard/blogger/post-blog.html')

@is_blogger
@login_required
def all_blog(request):
    return render(request, 'dashboard/blogger/all-blog.html')