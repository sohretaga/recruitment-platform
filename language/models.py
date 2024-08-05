from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

class Translation(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField()
    translation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('language', 'text')