from django.db import models
from recruitment_cp.models import ParameterFAQ
from user.models import CustomUser

# Create your models here.

class FAQ(models.Model):
    category = models.ForeignKey(ParameterFAQ, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

class Notification(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_sent')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_received')
    content = models.CharField(max_length=100)
    read = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
