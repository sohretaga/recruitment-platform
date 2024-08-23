from . import models
from django.db.models import OuterRef, Case, Value, When, F, IntegerField
from django.db.models.functions import Cast
from datetime import datetime

def manage_user_type_for_details(request, username:str, user_type:str) -> dict:
    user_exists = models.CustomUser.objects.filter(username=username).exists()
    user_is_superuser = False
    if user_exists:
        user_is_superuser = models.CustomUser.objects.get(username=username).is_superuser

    if request.user.is_superuser or user_is_superuser:
        params = {
            'username': username,
        }
    else:
        params = {
            'username': username,
            'user_type': user_type
        }
    
    return params

def calculate_recent_duration(model):
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_mapping = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    latest_duration = model.objects.filter(
        candidate=OuterRef('pk')
    ).order_by('start_date_year', 'start_date_month').annotate(
        start_year_int=Cast(F('start_date_year'), output_field=IntegerField()),
        start_month_int=Case(
            *[When(start_date_month=month, then=Value(num)) for month, num in month_mapping.items()],
            output_field=IntegerField()
        )
    ).annotate(
        years_diff=Value(current_year, output_field=IntegerField()) - F('start_year_int'),
        months_diff=Value(current_month, output_field=IntegerField()) - F('start_month_int')
    ).annotate(
        total_diff=F('years_diff') + (F('months_diff') / 12.0)
    ).values('total_diff')[:1]

    return latest_duration