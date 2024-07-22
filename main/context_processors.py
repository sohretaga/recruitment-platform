def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications_received.filter(read=False).count()
    else:
        count = False

    return {'notification_count':count}