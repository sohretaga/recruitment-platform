from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django.core.cache import cache
from froala_editor.fields import FroalaField

# Create your models here.

class Category(models.Model):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500)
    definition = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)

class Blog(models.Model):

    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('deactivated', 'Deactivated')
    ]

    title_en = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cover_photo = models.ImageField(upload_to='blog/cover', null=True, blank=True)
    content_en = FroalaField()
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
        language = cache.get('site_language', 'en')
        match language:
            case 'en':
                blogs = cls.objects.annotate(
                    title = F('title_en'),
                    content = F('content_en')
                )
            case 'tr':
                blogs = cls.objects.annotate(
                )
        return blogs.all()