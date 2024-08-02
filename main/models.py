from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content = models.CharField(max_length=100)
    read = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class ContactEmail(models.Model):
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email

class Subscribe(models.Model):
    email = models.EmailField()
    subscribe_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email

class HowItWork(models.Model):
    no = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='how-it-work/')

    class Meta:
        ordering = ['no']

    def __str__(self) -> str:
        return self.title

class Team(models.Model):
    full_name = models.CharField(max_length=150)
    profession = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team-image/')
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.full_name
