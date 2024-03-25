from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Employer, Candidate


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'employer':
            Employer.objects.create(user=instance)

        elif instance.user_type == 'candidate':
            Candidate.objects.create(user=instance)