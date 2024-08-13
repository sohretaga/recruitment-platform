from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from recruitment import settings
from blog.models import Blog, Comment, Category

from dashboard.decorators import is_blogger
from dashboard.forms import PostBlogForm

import os

@is_blogger
def post_blog(request):
    if request.POST:
        form = PostBlogForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:all-blog'))
    
    categories = Category.translation()

    context = {
        'categories': categories
    }

    return render(request, 'dashboard/blogger/post-blog.html', context)

@is_blogger
def all_blog(request):
    blogs = Blog.translation()

    context = {
        'blogs': blogs,
    }

    return render(request, 'dashboard/blogger/all-blog.html', context)

@is_blogger
def comments(request):
    comments = Comment.translation()

    context = {
        'comments': comments,
    }

    return render(request, 'dashboard/blogger/comments.html', context)

@require_POST
def ajax_delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.filter(id=comment_id)
    comment.delete()

    return JsonResponse({'status':200})

@require_POST
def ajax_edit_comment(request):
    comment_id = request.POST.get('comment_id')
    edited_comment = request.POST.get('edited_comment')
    comment = get_object_or_404(Comment, id=comment_id)
    comment.comment = edited_comment
    comment.save()

    return JsonResponse({'status':200})

@is_blogger
def ajax_manage_comment_status(request):
    comment_id = request.POST.get('comment_id')
    status = request.POST.get('status')
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = status
    comment.save()

    return JsonResponse({'status': 200})

@is_blogger
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    categories = Category.translation()

    if request.POST:
        form = PostBlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:all-blog'))

    context = {
        'blog': blog,
        'categories': categories
    }

    return render(request, 'dashboard/blogger/post-blog.html', context)

@require_POST
def ajax_delete_blog(request):
    blog_id = request.POST.get('blog_id')
    blog = Blog.objects.filter(id=blog_id)
    blog.delete()

    return JsonResponse({'status':200})

@csrf_exempt
def upload_editor_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        file = request.FILES['upload']
        upload_path = os.path.join(settings.MEDIA_ROOT, settings.CKEDITOR_UPLOAD_PATH)

        # Check and create the upload path if it does not exist
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Save the image to the path
        storage = FileSystemStorage(location=upload_path)
        image = storage.save(file.name, file)

        # Make the image URL
        image_url = settings.MEDIA_URL + settings.CKEDITOR_UPLOAD_PATH + '/' + file.name
        
        response = {
            'uploaded': True,
            'fileName': file.name,
            'url': image_url
        }

        return JsonResponse(response)
    else:
        response = {
            'uploaded': False,
            'error': {
                'message': 'No file uploaded or invalid request method.'
            }
        }
        return JsonResponse(response, status=400)