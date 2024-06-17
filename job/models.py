from django.db import models
from django.utils.text import slugify

from user.models import Employer, CustomUser
from recruitment_cp import models as cp_models

# Create your models here.

class Vacancy(models.Model):
    no = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=5)

    position_title = models.CharField(max_length=500, blank=True, null=True)

    employer = models.ForeignKey(Employer, related_name='vacancies', on_delete=models.CASCADE)
    career_type = models.ForeignKey(cp_models.ParameterCareerType, on_delete=models.SET_NULL, blank=True, null=True)
    career_level = models.ForeignKey(cp_models.ParameterCareerLevel, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(cp_models.ParameterLocation, on_delete=models.SET_NULL, blank=True, null=True)
    fte = models.ForeignKey(cp_models.ParameterFTE, on_delete=models.SET_NULL, blank=True, null=True)
    job_title = models.ForeignKey(cp_models.ParameterJobCatalogue, on_delete=models.SET_NULL, blank=True, null=True)
    employment_type = models.ForeignKey(cp_models.ParameterEmployeeType, on_delete=models.SET_NULL, blank=True, null=True)
    work_experience = models.ForeignKey(cp_models.ParameterWorkExperience, on_delete=models.SET_NULL, blank=True, null=True)
    work_preference = models.ForeignKey(cp_models.ParameterWorkPreference, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(cp_models.ParameterDepartment, on_delete=models.SET_NULL, blank=True, null=True)

    salary = models.IntegerField(default=0, null=True)
    salary_minimum = models.IntegerField(default=0, null=True)
    salary_midpoint = models.IntegerField(default=0, null=True)
    salary_maximum = models.IntegerField(default=0, null=True)

    definition = models.TextField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    status = models.BooleanField()
    views = models.IntegerField(default=0)
    slug = models.SlugField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

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

    def __str__(self) -> str:
        return self.position_title
    

class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)