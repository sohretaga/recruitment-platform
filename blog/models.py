from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    cover_photo = models.ImageField(upload_to='blog/cover')
    content = FroalaField()
    created_date = models.DateTimeField(auto_now_add=True)