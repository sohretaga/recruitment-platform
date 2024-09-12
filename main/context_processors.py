from language.middleware import get_current_user_language

def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications_received.filter(read=False).count()
    else:
        count = False

    return {'notification_count':count}

def selected_language(request):
    language_code = get_current_user_language()
    return {'language_code': language_code}