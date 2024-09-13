from django.db import models
from django.db.models import F

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

class Translation(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField()
    translation_en = models.TextField(null=True, blank=True)
    translation_tr = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('language', 'text')
        ordering = ('id',)

    @classmethod
    def translation(cls, language_code):
        translation = cls.objects.annotate(
            translated_text = F(f'translation_{language_code}')
        )

        return translation