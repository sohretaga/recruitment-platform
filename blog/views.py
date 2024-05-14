from django.shortcuts import render
from .models import Blog
from django.core.paginator import Paginator

# Create your views here.

def blog(request):


    # Set up Paginator
    paginator = Paginator(Blog.objects.all(), 8)
    current_page = request.GET.get('page')
    blogs = paginator.get_page(current_page)

    context = {
        'blogs': blogs,
    }
    
    return render(request, 'blog/blog.html', context)

def detail(request, slug):
    blog = Blog.objects.get(slug=slug)

    context = {
        'blog': blog
    }

    return render(request, 'blog/detail.html', context)