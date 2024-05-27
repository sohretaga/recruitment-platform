from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from recruitment import settings
from blog.models import Blog

from dashboard.decorators import is_blogger
from dashboard.forms import PostBlogForm

import os

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
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs
    }

    return render(request, 'dashboard/blogger/all-blog.html', context)

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