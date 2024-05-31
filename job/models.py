from django.db import models
from django.utils.text import slugify

from user.models import Employer

# Create your models here.

class Vacancy(models.Model):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500)
    definition = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=5)
    employer = models.ForeignKey(Employer, related_name='vacancies', on_delete=models.CASCADE)
    career_type = models.CharField(max_length=100, blank=True, null=True)
    career_level = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    fte = models.CharField(max_length=100, blank=True, null=True)
    salary = models.IntegerField(default=0, null=True)
    salary_minimum = models.IntegerField(default=0, null=True)
    salary_midpoint = models.IntegerField(default=0, null=True)
    salary_maximum = models.IntegerField(default=0, null=True)
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
            self.slug = slugify(self.position_title)
            original_slug = self.slug
            queryset = Vacancy.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Vacancy.objects.filter(slug=self.slug)
        super(Vacancy, self).save(*args, **kwargs)