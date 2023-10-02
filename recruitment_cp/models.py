from typing import Iterable, Optional
from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    is_default = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def save(self,*args, **kwargs) -> None:
        self.code = self.code.lower()
        super().save(*args, **kwargs)