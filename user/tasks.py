from celery import shared_task
from job.models import Vacancy

import json
import websocket

@shared_task()
def send_notification_to_preferred_candidates(vacancy_id, ws_protocol, host):
    vacancy = Vacancy.objects.get(id=vacancy_id)

    try:
        employer = vacancy.employer.preferred_employers.values_list('candidate__user__id', flat=True)
        career_type = vacancy.career_type.preferred_career_types.values_list('candidate__user__id', flat=True)
        location = vacancy.location.preferred_locations.values_list('candidate__user__id', flat=True)
        employment_type = vacancy.employment_type.preferred_employment_types.values_list('candidate__user__id', flat=True)

        common_candidates = set(employer).intersection(
            career_type,
            location,
            employment_type
        )

        for user_id in common_candidates:

            text_data = {
                "content": "PREFERRED",
                "related_data": vacancy_id,
            }

            target_ws_url = f"{ws_protocol}{host}/ws/send-notifications/{user_id}/"
            ws = websocket.create_connection(target_ws_url)
            ws.send(json.dumps(text_data))
            ws.close()
        
    except AttributeError: ...