from celery import shared_task
from django.utils import timezone
from .models import Vacancy, ExpiredVacancy

@shared_task
def move_expired_vacancies():
    now = timezone.now()
    expired_vacancies = Vacancy.objects.filter(ending_date__lt=now)

    for vacancy in expired_vacancies:
        ExpiredVacancy.objects.create(
            no=vacancy.no,
            language=vacancy.language,
            position_title=vacancy.position_title,
            employer=vacancy.employer,
            career_type=vacancy.career_type,
            career_level=vacancy.career_level,
            location=vacancy.location,
            fte=vacancy.fte,
            job_title=vacancy.job_title,
            employment_type=vacancy.employment_type,
            work_experience=vacancy.work_experience,
            work_preference=vacancy.work_preference,
            department=vacancy.department,
            salary=vacancy.salary,
            salary_minimum=vacancy.salary_minimum,
            salary_midpoint=vacancy.salary_midpoint,
            salary_maximum=vacancy.salary_maximum,
            keywords=vacancy.keywords,
            delete=vacancy.__dict__['delete'],
            views=vacancy.views,
            slug=vacancy.slug,
            approval_level=vacancy.approval_level,
            status=vacancy.status,
            anonium=vacancy.anonium,
            description=vacancy.description,
            responsibilities=vacancy.responsibilities,
            qualification=vacancy.qualification,
            skill_experience=vacancy.skill_experience,
            additional=vacancy.additional,
            created_date=vacancy.created_date,
            ending_date=vacancy.ending_date,
            published_date=vacancy.published_date,
        )

        vacancy.__class__.objects.filter(id=vacancy.id).delete()