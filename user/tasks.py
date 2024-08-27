from django.db.models import Q
from celery import shared_task
from job.models import Vacancy
from user.models import Candidate

import json
import websocket

@shared_task()
def send_notification_to_preferred_candidates(vacancy_id, ws_protocol, host):
    vacancy = Vacancy.objects.get(id=vacancy_id)

    try:
        employer = vacancy.employer.preferred_employers.values_list('candidate', flat=True)
        career_type = vacancy.career_type.preferred_career_types.values_list('candidate', flat=True)
        location = vacancy.location.preferred_locations.values_list('candidate', flat=True)
        employment_type = vacancy.employment_type.preferred_employment_types.values_list('candidate', flat=True)

        common_candidates = set(employer).intersection(
            career_type,
            location,
            employment_type
        )

        candidates = Candidate.objects.filter(
            # First condition: Is vacancy.salary within the candidate's preferred salary range?
            (
                Q(preference__min_salary__lte=vacancy.salary) &
                Q(preference__max_salary__gte=vacancy.salary)
            ) |
            (
                Q(preference__min_salary__lte=vacancy.salary_maximum) &
                Q(preference__max_salary__gte=vacancy.salary_minimum)
            ),
            # Second condition: Does the candidate's salary preference match the salary range of the job posting?
            id__in=common_candidates
        ).values_list('user__id', flat=True)

        for target_id in candidates:

            text_data = {
                "content": "PREFERRED",
                "related_data": vacancy_id,
            }

            target_ws_url = f"{ws_protocol}{host}/ws/send-notifications/{target_id}/"
            ws = websocket.create_connection(target_ws_url)
            ws.send(json.dumps(text_data))
            ws.close()
        
    except AttributeError: ...