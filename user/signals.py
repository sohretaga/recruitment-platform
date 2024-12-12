from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import CustomUser, Employer, Candidate, GalleryImage, ProjectImage

import os


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'employer':
            Employer.objects.create(user=instance)

        elif instance.user_type == 'candidate':
            Candidate.objects.create(user=instance)


@receiver(post_delete, sender=GalleryImage)
def delete_gallery_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=ProjectImage)
def delete_project_images(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)