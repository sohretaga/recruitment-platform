from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

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

class Service(models.Model):
    no = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='service/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['no']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Service.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Service.objects.filter(slug=self.slug)
        super(Service, self).save(*args, **kwargs)

# About Us Models

class AboutUs(models.Model):
    SECTION_CHOICES = [
        ('ABOUT_SECTION', 'About Section'),
        ('ABOUT_SECTION_FACTORS', 'About Section Factors'),
    ]

    section = models.CharField(max_length=25, choices=SECTION_CHOICES, unique=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self) -> str:
        return self.get_section_display()

class AboutSection(models.Model):
    about_us = models.OneToOneField(AboutUs, on_delete=models.CASCADE, related_name='about_section')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about-images/')

    def __str__(self):
        return self.title

class AboutSectionFactor(models.Model):
    about_section = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='factors')
    text = models.CharField(max_length=100)