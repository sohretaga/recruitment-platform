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

class ParameterCommonFields(models.Model):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500)
    definition = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=5)

    class Meta:
        abstract = True
        ordering = ['no']

class ParameterCareerType(ParameterCommonFields):
    ...

class ParameterCareerLevel(ParameterCommonFields):
    ...

class ParameterCareerTypeLevel(ParameterCommonFields):
    ...

class ParameterLocation(ParameterCommonFields):
    ...

class ParameterFTE(ParameterCommonFields):
    ...

class ParameterJobCatalogue(ParameterCommonFields):
    ...

class ParameterEmployeeType(ParameterCommonFields):
    ...

class ParameterVacancy(ParameterCommonFields):
    note = None
    organization = models.CharField(max_length=100, blank=True, null=True)
    career_type = models.CharField(max_length = 100, blank=True, null=True)
    career_level = models.CharField(max_length = 100, blank=True, null=True)
    location = models.CharField(max_length = 100, blank=True, null=True)
    fte = models.CharField(max_length = 100, blank=True, null=True)
    salary_minimum = models.IntegerField(default=0)
    salary_midpoint = models.IntegerField(default=0)
    salary_maximum = models.IntegerField(default=0)
    job_catalogue = models.CharField(max_length = 100, blank=True, null=True)
    position_title = models.CharField(max_length = 100, blank=True, null=True)
    job_title = models.CharField(max_length = 100, blank=True, null=True)
    employment_type = models.CharField(max_length = 100, blank=True, null=True)
    definition = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)