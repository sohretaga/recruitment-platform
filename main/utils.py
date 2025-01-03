from django.urls import reverse
from django.db.models import F
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.timesince import timesince

from collections import Counter
from job.models import Vacancy
from recruitment_cp.models import ParameterKeyword
from main.models import Notification, ContactEmail
from language.utils import tr

import math
import datetime

def get_vacancy_in_sublists(objects_per_list=5) -> list:
    objects = list(Vacancy.translation().filter(status=True, delete=False, approval_level='PUBLISHED').order_by('?')[:10])
    
    total_objects = len(objects)
    
    number_of_lists = math.ceil(total_objects / objects_per_list)
    
    sublists = [
        objects[i * objects_per_list:(i + 1) * objects_per_list]
        for i in range(number_of_lists)
    ]

    return sublists

def get_trending_keywords():
    vacancies = Vacancy.translation().all()
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

def humanize_time(value) -> str:
    if value:
        now = datetime.datetime.now(datetime.timezone.utc)
        diff = now - value
        if diff.days >= 1:
            translated_month_name = tr(value.strftime('%B'))
            return f'{value.day} {translated_month_name}, {value.year}'
        
        # minute and hour translation is done with the tr function.
        vavlue_str = timesince(value)\
            .replace('hours', tr('hours'))\
            .replace('minutes', tr('minutes'))
        
        return vavlue_str

def fetch_notifications(objects):
    notifications = list()

    for n in objects:
        from_user_type = n.from_user.user_type
        to_user_type = n.to_user.user_type
        profile_photo = n.from_user.profile_photo
        content_object = n.content_object
        content = n.content
        content_display = tr(n.get_content_display()) # translation is done with the tr function
        related_data = False

        if profile_photo:
            profile_photo = profile_photo.url

        if content == 'PREFERRED' and content_object:

            # If the vacancy is not published for any reason (status, delete, approval level),
            # it cannot be clicked on the notification bar.
            if content_object.status == True and\
                content_object.delete == False and\
                content_object.approval_level == 'PUBLISHED':

                related_data = reverse('job:vacancy', args=[content_object.slug])
            
            title = content_object.position_title
        else:        
            if to_user_type == 'employer' and content_object:
                related_data = reverse('job:applicants', args=[content_object.vacancy.slug])

            elif to_user_type == 'candidate' and content_object:
                related_data = reverse('job:applications')

            if from_user_type == 'employer':
                title = n.from_user.first_name

            elif from_user_type == 'candidate':
                title = f'{n.from_user.first_name} {n.from_user.last_name}'

        notifications.append({
            'id': n.id,
            'user_type': to_user_type,
            'profile_photo': profile_photo,
            'title': title,
            'related_data': related_data,
            'content': content_display,
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