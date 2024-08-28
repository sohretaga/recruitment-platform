from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.core.cache import cache
from django.conf import settings
from django.db.models import F
from ckeditor_uploader.fields import RichTextUploadingField

from recruitment_cp.models import ParameterFAQ
from user.models import CustomUser
from job.models import CandidateAction, EmployerAction

# Create your models here.

class FAQ(models.Model):
    category = models.ForeignKey(ParameterFAQ, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()


class Notification(models.Model):
    # For translation, the same texts must be written in translation.html
    CONTENT_CHOICES = [
        # Types of notifications from candidates
        ('APPLY', 'Applied to your vacancy - NOTIFICATION'),
        ('DELETE_APPLY', 'Deleted application for your vacancy - NOTIFICATION'),
        *CandidateAction.ACTION_CHOICES,

        # Types of notifications from employers
        ('PREFERRED', 'New vacancy that match your preferences are available - NOTIFICATION'),
        *EmployerAction.ACTION_CHOICES,
    ]

    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_sent')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_received')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content = models.CharField(max_length=25, choices=CONTENT_CHOICES)
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
    title_en = models.CharField(max_length=255, verbose_name='Title EN')
    title_tr = models.CharField(max_length=255, verbose_name='Title TR')

    description_en = models.TextField(verbose_name='Description EN')
    description_tr = models.TextField(verbose_name='Description TR')

    image = models.ImageField(upload_to='how-it-work/')

    class Meta:
        ordering = ['no']

    def __str__(self) -> str:
        return self.title_en
    
    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                how_it_work = cls.objects.annotate(
                    title = F('title_en'),
                    description = F('description_en')
                ).all()
            case 'tr':
                how_it_work = cls.objects.annotate(
                    title = F('title_tr'),
                    description = F('description_tr')
                ).all()
        return how_it_work

class Team(models.Model):
    full_name = models.CharField(max_length=150)
    about_en = models.TextField(blank=True, null=True, verbose_name='About EN')
    about_tr = models.TextField(blank=True, null=True, verbose_name='About TR')

    profession = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team-image/')
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.full_name
    
    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                members = cls.objects.annotate(
                    about = F('about_en'),
                )
            case 'tr':
                members = cls.objects.annotate(
                    about = F('about_tr'),
                )
        return members.all()

class Service(models.Model):
    no = models.PositiveIntegerField()
    title_en = models.CharField(max_length=255, verbose_name='Title EN')
    title_tr = models.CharField(max_length=255, verbose_name='Title TR')

    description_en = RichTextUploadingField(default='', verbose_name='Description EN')
    description_tr = RichTextUploadingField(default='', verbose_name='Description TR')

    icon = models.ImageField(upload_to='service/', blank=True, null=True)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['no']

    def __str__(self) -> str:
        return self.title_en

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title_en)
            original_slug = self.slug
            queryset = Service.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Service.objects.filter(slug=self.slug)
        super(Service, self).save(*args, **kwargs)

    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                services = cls.objects.annotate(
                    title = F('title_en'),
                    description = F('description_en')
                ).all()
            case 'tr':
                services = cls.objects.annotate(
                    title = F('title_tr'),
                    description = F('description_tr')
                ).all()
        return services

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
    title_en = models.CharField(max_length=200, verbose_name='Title EN')
    title_tr = models.CharField(max_length=200, verbose_name='Title TR')

    description_en = models.TextField(verbose_name='Description EN')
    description_tr = models.TextField(verbose_name='Description TR')

    image = models.ImageField(upload_to='about-images/')

    def __str__(self):
        return self.title_en
    
    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                sections = cls.objects.annotate(
                    title = F('title_en'),
                    description = F('description_en')
                )
            case 'tr':
                sections = cls.objects.annotate(
                    title = F('title_tr'),
                    description = F('description_tr')
                )
        return sections.all()

class AboutSectionFactor(models.Model):
    about_section = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='factors')
    text_en = models.CharField(max_length=100, verbose_name='Title EN')
    text_tr = models.CharField(max_length=100, verbose_name='Title TR')

    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                factors = cls.objects.annotate(
                    text = F('text_en'),
                )
            case 'tr':
                factors = cls.objects.annotate(
                    text = F('text_tr'),
                )
        return factors.all()