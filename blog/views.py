from django.shortcuts import render
from .models import Blog, Category
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.

def blog(request):

    # Set up Paginator
    all_blogs = Blog.objects.filter(status='published').order_by('created_date')
    paginator = Paginator(all_blogs, 8)
    current_page = request.GET.get('page')
    blogs = paginator.get_page(current_page)

    categories = Category.objects.all()

    context = {
        'blogs': blogs,
        'categories': categories
    }
    
    return render(request, 'blog/blog.html', context)

def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.views += 1
    blog.save()

    if blog.status != 'published' and not request.user.is_superuser:
        raise Http404

    context = {
        'blog': blog
    }

    return render(request, 'blog/detail.html', context)