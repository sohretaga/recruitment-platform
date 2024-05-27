from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField

# Create your models here.

class Blog(models.Model):

    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('deactivated', 'Deactivated')
    ]

    title = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    cover_photo = models.ImageField(upload_to='blog/cover')
    content = FroalaField()
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)