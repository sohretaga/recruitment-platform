from collections import Counter
from job.models import Vacancy
from recruitment_cp.models import ParameterKeyword
from main.models import Notification
import math

def get_vacancy_in_sublists(objects_per_list=5) -> list:
    objects = list(Vacancy.objects.filter(status=True, delete=False).order_by('?')[:10])
    
    total_objects = len(objects)
    
    number_of_lists = math.ceil(total_objects / objects_per_list)
    
    sublists = [
        objects[i * objects_per_list:(i + 1) * objects_per_list]
        for i in range(number_of_lists)
    ]

    return sublists

def get_trending_keywords():
    vacancies = Vacancy.objects.all()
    all_keywords = []

    for vacancy in vacancies:
        if vacancy.keywords:
            for keyword in vacancy.keywords:
                if isinstance(keyword, list):
                    all_keywords.extend(keyword)
                else:
                    all_keywords.append(keyword)
    
    keyword_counter = Counter(all_keywords)

    # En çok kullanılan 5 keyword
    most_common_keywords = keyword_counter.most_common(5)

    # Keyword ID'leri yerine isimlerini almak isterseniz
    most_common_keyword_ids = [keyword_id for keyword_id, count in most_common_keywords]
    most_common_keyword_names = ParameterKeyword.objects.filter(id__in=most_common_keyword_ids).values_list('name', flat=True)

    return most_common_keyword_names

def mark_notifications_as_read(request) -> None:
    unread_notifictions = request.user.notifications_received.filter(read=False)
    if unread_notifictions:
        for read in unread_notifictions:
            read.read = True

        Notification.objects.bulk_update(unread_notifictions, ['read'])


from django.utils.timesince import timesince
import datetime

def humanize_time(value):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - value
    if diff.days >= 1:
        return value.strftime('%d %b, %Y')
    
    return timesince(value)

def fetch_notifications(objects) -> list:
    notifications_list = []
    for notification in objects:
        related_object = notification.related_object
        vacancy_slug = related_object.vacancy.slug if related_object else False

        related_data = {
            'id': notification.id,
            'user_type': notification.to_user.user_type,
            'profile_photo': notification.from_user.profile_photo,
            'full_name':notification.from_user.get_full_name(),
            'content': notification.content,
            'vacancy_slug': vacancy_slug,
            'timestamp': humanize_time(notification.timestamp)
        }

        notifications_list.append(related_data)

    return notifications_list