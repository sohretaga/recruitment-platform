from django.db.models.signals import post_delete
from django.dispatch import receiver
from job.models import Apply
import os

@receiver(post_delete, sender=Apply)
def delete_cv_file(sender, instance, **kwargs):
    if instance.cv:
        if os.path.isfile(instance.cv.path):
            os.remove(instance.cv.path)
