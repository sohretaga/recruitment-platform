from django.db import models
from django.utils.text import slugify

from user.models import CustomUser

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

class ParameterCountry(ParameterCommonFields):
    ...

class ParameterLocation(ParameterCommonFields):
    ...

class ParameterWorkExperience(ParameterCommonFields):
    ...

class ParameterFTE(ParameterCommonFields):
    ...

class ParameterJobCatalogue(ParameterCommonFields):
    """
    - Job Title is name field
    - Common Duties and Responsibilities is definition field
    """

    job_family = models.CharField(max_length=100, blank=True, null=True)
    job_sub_family = models.CharField(max_length=100, blank=True, null=True)
    career_type = models.CharField(max_length=100, blank=True, null=True)
    career_level = models.CharField(max_length=100, blank=True, null=True)
    typical_education = models.CharField(max_length=100, blank=True, null=True)
    relevant_experience = models.CharField(max_length=100, blank=True, null=True)
    job_code = models.CharField(max_length=100, blank=True, null=True)

class ParameterEmployeeType(ParameterCommonFields):
    ...

class ParameterVacancy(ParameterCommonFields):
    note = None
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    career_type = models.CharField(max_length=100, blank=True, null=True)
    career_level = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    fte = models.CharField(max_length=100, blank=True, null=True)
    salary = models.IntegerField(default=0)
    salary_minimum = models.IntegerField(default=0)
    salary_midpoint = models.IntegerField(default=0)
    salary_maximum = models.IntegerField(default=0)
    job_catalogue = models.CharField(max_length=100, blank=True, null=True)
    position_title = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    employment_type = models.CharField(max_length=100, blank=True, null=True)
    work_experience = models.CharField(max_length=100, blank=True, null=True)
    definition = models.TextField()
    views = models.IntegerField(default=0)
    slug = models.SlugField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.job_title)
            original_slug = self.slug
            queryset = ParameterVacancy.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = ParameterVacancy.objects.filter(slug=self.slug)
        super(ParameterVacancy, self).save(*args, **kwargs)