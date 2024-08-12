from django.db import models
from django.utils.text import slugify
from django.core.cache import cache
from django.db.models import F, Value, CharField
from froala_editor.fields import FroalaField
from django.conf import settings

from recruitment_cp.models import ParameterCommonFields
from user.models import CustomUser

# Create your models here.

class Category(ParameterCommonFields):
    ...

class Blog(models.Model):

    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('deactivated', 'Deactivated')
    ]

    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title EN')
    title_tr = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title TR')

    content_en = FroalaField(blank=True, null=True)
    content_tr = FroalaField(blank=True, null=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cover_photo = models.ImageField(upload_to='blog/cover', null=True, blank=True)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    quick_career_tip = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title_en

    def save(self, *args, **kwargs) -> None:
        if not self.slug:  # Only create slug if it's not set
            self.slug = slugify(self.title_en)
            original_slug = self.slug
            queryset = Blog.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Blog.objects.filter(slug=self.slug)
        super(Blog, self).save(*args, **kwargs)

    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                blogs = cls.objects.annotate(
                    title = F('title_en'),
                    content = F('content_en'),
                    category_name = F('category__name_en'),
                    language = Value(value=language, output_field=CharField())
                )
            case 'tr':
                blogs = cls.objects.annotate(
                    title = F('title_tr'),
                    content = F('content_tr'),
                    category_name = F('category__name_tr'),
                    language = Value(value=language, output_field=CharField())
                )
        return blogs.all()
    
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = (('blog', 'user'), ('blog', 'session_id'))

class Comment(models.Model):
    STATUS_CHOICES = [
        ('PUBLISHED', 'Published'),
        ('PENDING', 'Pending'),
        ('DEACTIVATED', 'Deactivated')
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-id']

    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                comments = cls.objects.annotate(
                    blog_title = F('blog__title_en'),
                )
            case 'tr':
                comments = cls.objects.annotate(
                    blog_title = F('blog__title_tr'),
                )
        return comments.all()