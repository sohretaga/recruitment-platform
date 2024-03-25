from django.db.models.signals import post_save
from django.dispatch import receiver

from models import CustomUser, Employer, Candidate


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type.get_user_type_display() == 'empolyer':
            Employer.objects.create(user=instance)

        elif instance.user_type.get_user_type_display() == 'candidate':
            Candidate.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type.get_user_type_display() == 'empolyer':
        instance.employer.save()

    elif instance.user_type.get_user_type_display() == 'candidate':
        instance.candidate.save()