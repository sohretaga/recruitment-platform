from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404

from .models import Blog, Like, Category
from recruitment_cp.utils import is_ajax

import json

# Create your views here.

def blog(request):
    # URL parameters are taken for filtering and used for the same filtering on the following pages.
    categories:str|None = request.GET.get('categories')
    params:dict = {'status':'published'} # only get pusblised blogs
    url:str = '' # Creating URL for Pagination

    if categories:
        url += f'&categories={categories}'
        params.update({'category_name__in': categories.split(',')})

    # Set up Paginator
    all_blogs = Blog.translation().filter(**params).order_by('created_date')
    paginator = Paginator(all_blogs, 8)
    current_page = request.GET.get('page')
    blogs = paginator.get_page(current_page)

    categories = Category.translation()

    # Popular Blogs
    pobular_blogs = Blog.translation().filter(status='published').order_by('-views')[:4]

    context = {
        'blogs': blogs,
        'pobular_blogs': pobular_blogs,
        'categories': categories,
        'url': url
    }
    
    return render(request, 'blog/blog.html', context)

def detail(request, slug):
    categories = Category.translation()
    blog = Blog.translation().get(slug=slug)
    blog.views += 1
    blog.save()

    if blog.status != 'published' and not request.user.is_superuser:
        raise Http404

    # Blogs
    pobular_blogs = Blog.translation().filter(status='published').order_by('-views')[:4]
    all_blogs = Blog.translation().filter(status='published').exclude(slug=slug)

    # Blog Like
    session_id = request.session.session_key
    
    if request.user.is_authenticated:
        user = request.user
        like_exists = Like.objects.filter(blog=blog, user=user).exists()
    else:
        user = None
        like_exists = Like.objects.filter(blog=blog, session_id=session_id).exists()

    context = {
        'blog': blog,
        'categories': categories,
        'pobular_blogs': pobular_blogs,
        'all_blogs': all_blogs,
        'like': like_exists
    }

    return render(request, 'blog/detail.html', context)

@require_POST
def ajax_filter_blog(request):
    if is_ajax:
        data = json.loads(request.body.decode('utf-8'))
        categories = data.get('categories', [])

        params = {'status':'published'} # only get pusblised blogs

        if categories:
            params.update({'category_name__in':categories})        

        filtered_blogs = Blog.translation().filter(**params).order_by('created_date')\
        .values('title', 'category_name', 'cover_photo', 'views', 'slug', 'created_date')
        
        # Set up Paginator
        paginator = Paginator(filtered_blogs, 8)
        current_page_number = request.POST.get('page', 1)
        blogs_page = paginator.get_page(current_page_number)

        # Serialize the data
        blog_list = list(blogs_page.object_list.values())

        pagination_info = {
            'has_next': blogs_page.has_next(),
            'has_previous': blogs_page.has_previous(),
            'num_pages': blogs_page.paginator.num_pages,
            'current_page': blogs_page.number,
        }

        context = {
            'blogs': blog_list,
            'pagination': pagination_info
        }

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def ajax_like_blog(request):
    blog_id = request.POST.get('blog_id')
    blog = get_object_or_404(Blog, id=blog_id)
    session_id = request.session.session_key

    def like_manager(params):
        global action

        if like_exists:
            Like.objects.filter(**params).delete()
            action = 'dislike'
        else:
            Like.objects.create(**params)
            action = 'like'

    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    if request.user.is_authenticated:
        user = request.user
        like_exists = Like.objects.filter(blog=blog, user=user).exists()

        like_manager({
            'blog': blog,
            'user': user
        })
    else:
        like_exists = Like.objects.filter(blog=blog, session_id=session_id).exists()

        like_manager({
            'blog': blog,
            'session_id': session_id
        })


    count = blog.likes.count()

    return JsonResponse({
        "action": action,
        'count': count
    })