from django.db import models
from django.db.models import F

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

class Translation(models.Model):
    text = models.CharField(max_length=255, unique=True)
    translation_en = models.TextField(null=True, blank=True)
    translation_tr = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('id',)

    @classmethod
    def translation(cls, language_code):
        translation = cls.objects.annotate(
            translated_text = F(f'translation_{language_code}')
        )

        return translation