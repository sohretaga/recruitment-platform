from language.middleware import get_current_user_language
from job.models import Vacancy

def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications_received.filter(read=False).count()
    else:
        count = False

    return {'notification_count':count}

def selected_language(request):
    language_code = get_current_user_language()
    return {'language_code': language_code}

def marquee(request):
    marquees = Vacancy.translation().filter(status=True, delete=False, approval_level='PUBLISHED', type='PREMIUM')\
        .values('position_title', 'slug', 'employer__user__first_name')
    return {'marquees': marquees}