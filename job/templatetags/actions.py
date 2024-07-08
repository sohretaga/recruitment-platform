from django import template
from job.models import Bookmark, Apply

register = template.Library()

@register.simple_tag
def bookmarks(request, vacancy_id) -> str:
    if request.user.is_authenticated:
        bookmarks_exists = Bookmark.objects.filter(user=request.user, vacancy__id=vacancy_id).exists()
        if bookmarks_exists:
            return 'bookmark-post'
    return ''
        
@register.simple_tag
def applications(request, vacancy_id) -> bool:
    user = request.user
    if user.is_authenticated and user.user_type == 'candidate':
        apply_exists = Apply.objects.filter(candidate=request.user.candidate, vacancy__id=vacancy_id).exists()
        return apply_exists
    return False