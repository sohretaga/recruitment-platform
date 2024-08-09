from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST

from recruitment import settings
from blog.models import Blog, Category

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

def upload_editor_image(request):
    if request.POST and request.FILES.get('file'):
        file = request.FILES['file']
        upload_path = os.path.join(settings.MEDIA_ROOT, settings.FROALA_UPLOAD_PATH)

        # Check path
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Save image to path
        storage = FileSystemStorage(location=upload_path)
        image = storage.save(file.name, file)

        # Make image url
        protocol = 'https://' if request.is_secure() else 'http://'
        domain_url = protocol + request.META.get('HTTP_HOST', '')
        image_url = domain_url + settings.MEDIA_URL + settings.FROALA_UPLOAD_PATH + f'/{image}'

        return JsonResponse({'link': image_url})
    
def delete_editor_image(request):
    if request.POST:
        src = request.POST.get('src', None)
        if src:
            image_url = src.split('/media/')[-1]
            image_path = os.path.join(settings.MEDIA_ROOT, image_url)

            if os.path.exists(image_path):
                os.remove(image_path)
                return JsonResponse({'message': 'The image has been deleted successfully.'})
            else:
                return JsonResponse({'error': 'The specified image was not found.'}, status=404)

    return HttpResponse()