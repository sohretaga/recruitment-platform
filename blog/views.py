from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Count, Value, Case, When, BooleanField, Exists, OuterRef

from .models import Blog, Like, Comment, Category
from recruitment_cp.utils import is_ajax
from main.utils import humanize_time

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
    pobular_blogs = Blog.translation().filter(status='published').exclude(slug=slug).order_by('-views')[:4]
    all_blogs = Blog.translation().filter(status='published').exclude(slug=slug)

    # Comments
    if request.user.is_authenticated:
        comments = blog.comments.filter(Q(status='PUBLISHED') | Q(user=request.user))
    else:
        comments = blog.comments.filter(Q(status='PUBLISHED'))

    comments_count = blog.comments.filter(status='PUBLISHED').count()

    context = {
        'blog': blog,
        'categories': categories,
        'pobular_blogs': pobular_blogs,
        'all_blogs': all_blogs,
        'comments': comments,
        'comments_count': comments_count
    }

    return render(request, 'blog/detail.html', context)

@require_POST
def ajax_filter_blog(request):
    if is_ajax:
        data = json.loads(request.body.decode('utf-8'))
        categories = data.get('categories', [])

        params = {'status':'published'} # only get pusblised blogs

        user_id = request.user.id if request.user.is_authenticated else None
        session_id = request.session.session_key

        user_liked_blog = Like.objects.filter(
            blog=OuterRef('pk'),
            user_id=user_id
        )

        session_liked_blog = Like.objects.filter(
            blog=OuterRef('pk'),
            session_id=session_id
        )

        if categories:
            params['category_name__in'] = categories    

        filtered_blogs = Blog.translation().filter(**params).annotate(
            like_count=Count('likes'),
            is_liked=Case(
                When(Exists(user_liked_blog), then=Value(True)),
                When(Exists(session_liked_blog), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('created_date').values('id', 'title', 'category_name', 'cover_photo', 'views', 'slug', 'created_date', 'like_count', 'is_liked')
        
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

@require_POST
def ajax_send_comment(request):
    blog_id = request.POST.get('blog_id')
    new_comment = request.POST.get('comment')
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user.is_authenticated and new_comment:
        comment = Comment.objects.create(
            blog=blog,
            user=request.user,
            comment=new_comment
        )

        context = {
            "id": comment.id,
            "user_full_name": comment.user.get_full_name(),
            "username": comment.user.username,
            "user_profile_photo": comment.user.profile_photo.url if comment.user.profile_photo else None,
            "comment": comment.comment,
            "timestamp": humanize_time(comment.timestamp),
            "comment_count": blog.comments.filter(status='PUBLISHED').count()
        }
    
        return JsonResponse(context, safe=False)
    else:
        return JsonResponse({'status':500})

@require_POST
def ajax_delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        comment.delete()

    blog_comment_count = comment.blog.comments.filter(status='PUBLISHED').count()

    context = {
        "comment_count": blog_comment_count
    }
    
    return JsonResponse(context)

@require_POST
def ajax_edit_comment(request):
    comment_id = request.POST.get('comment_id')
    edited_comment = request.POST.get('edited_comment')
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        comment.comment = edited_comment
        comment.status = 'PENDING'
        comment.save()
    
    blog_comment_count = comment.blog.comments.filter(status='PUBLISHED').count()

    context = {
        "edited_comment": edited_comment,
        "comment_count": blog_comment_count
    }
    
    return JsonResponse(context)