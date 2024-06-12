from django import template
from job.models import Bookmark

register = template.Library()

@register.simple_tag
def bookmarks(request, id):
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(user=request.user).values_list('vacancy__id', flat=True)
        if id in bookmarks:
            return 'bookmark-post'