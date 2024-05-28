from django.db import models
from django.utils.text import slugify
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

    title = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cover_photo = models.ImageField(upload_to='blog/cover', null=True, blank=True)
    content = FroalaField()
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def category_name(self) -> str:
        return self.category.name

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)