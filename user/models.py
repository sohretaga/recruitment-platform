from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
        ('blogger', 'Content'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_registration_complete = models.BooleanField(default=False, editable=False)
    terms = models.BooleanField()

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate')

    def __str__(self) -> str:
        return self.user.username

class Company(models.Model):
    employer = models.OneToOneField(Employer, models.CASCADE, related_name='company', null=True)
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=200, blank=True, null=True)
    organization_type = models.CharField(max_length=200, blank=True, null=True)
    organization_ownership = models.CharField(max_length=200, blank=True, null=True)
    number_of_employees = models.CharField(max_length=15, blank=True, null=True)
    primary_email = models.EmailField(blank=True, null=True)
    second_email = models.EmailField(blank=True, null=True)
    other_email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            queryset = Company.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Company.objects.filter(slug=self.slug)
        super(Company, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name