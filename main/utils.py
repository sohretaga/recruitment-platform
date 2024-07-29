from django.urls import reverse
from django.db.models import F
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from collections import Counter
from job.models import Vacancy
from recruitment_cp.models import ParameterKeyword
from main.models import Notification, ContactEmail
import math
import time

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

def fetch_notifications(objects):
    notifications = list()

    for n in objects:
        user_type = n.to_user.user_type
        profile_photo = n.from_user.profile_photo

        if profile_photo:
            profile_photo = profile_photo.url
        
        if user_type == 'employer':
            related_data = reverse('job:applicants', args=[n.related_data])
        elif user_type == 'candidate':
            related_data = reverse('job:applications')

        notifications.append({
            'id': n.id,
            'user_type': n.to_user.user_type,
            'profile_photo': profile_photo,
            'full_name': n.from_user.get_full_name(),
            'related_data': related_data,
            'content': n.content,
            'timestamp': humanize_time(n.timestamp)
        })

    return notifications


def send_contact_email(name, email, subject, message):
    content = get_template('main/contact-email-template.html').render({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })

    contact_emails = ContactEmail.objects.values_list('email', flat=True)

    for contact_email in contact_emails:
        mail = EmailMultiAlternatives(
            "New Contact",
            f"Message: {message}",
            "Recruitment Contact <contact@sohretaga.com>",
            [contact_email]
        )

        mail.attach_alternative(content, "text/html")
        mail.send()

        time.sleep(1)