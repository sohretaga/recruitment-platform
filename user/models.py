from django.db import models
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer', blank=True, null=True) # blank=True, null=True will delete
    no = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=200, blank=True, null=True)
    organization_type = models.CharField(max_length=200, blank=True, null=True)
    organization_ownership = models.CharField(max_length=200, blank=True, null=True)
    number_of_employees = models.CharField(max_length=15, blank=True, null=True)
    second_email = models.EmailField(blank=True, null=True)
    other_email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.company_name

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate')

    def __str__(self) -> str:
        return self.user.username