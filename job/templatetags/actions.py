from django import template
from job.models import Bookmark, Apply
from user.models import CandidateBookmark

register = template.Library()

@register.simple_tag
def bookmarks(request, vacancy_id) -> str:
    if request.user.is_authenticated:
        bookmarks_exists = Bookmark.objects.filter(user=request.user, vacancy__id=vacancy_id).exists()
        if bookmarks_exists:
            return 'bookmark-post'
    return ''

@register.simple_tag
def candidate_bookmarks(request, candidate_id) -> str:
    if request.user.is_authenticated and request.user.user_type == 'employer':
        candidate_bookmarks_exists = CandidateBookmark.objects.filter(employer=request.user.employer, candidate__id=candidate_id).exists()
        if candidate_bookmarks_exists:
            return 'bookmark-post'
    return ''
        
@register.simple_tag
def applications(request, vacancy_id) -> bool:
    user = request.user
    if user.is_authenticated and user.user_type == 'candidate':
        apply_exists = Apply.objects.filter(candidate=request.user.candidate, vacancy__id=vacancy_id).exists()
        return apply_exists
    return False