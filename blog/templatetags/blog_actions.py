from django import template
from blog.models import Like

register = template.Library()

@register.simple_tag
def liked(request, blog_id) -> str:
    session_id = request.session.session_key

    if request.user.is_authenticated:
        user = request.user
        like_exists = Like.objects.filter(blog__id=blog_id, user=user).exists()
    else:
        like_exists = Like.objects.filter(blog__id=blog_id, session_id=session_id).exists()
    
    return 'liked' if like_exists else ''