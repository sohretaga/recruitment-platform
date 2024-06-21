from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
        ('blogger', 'Content'),
    )

    profile_photo = models.ImageField(upload_to='profile-photos/', null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_registration_complete = models.BooleanField(default=False, editable=False)
    terms = models.BooleanField()

class Employer(models.Model):
    """
    The company name is recorded in the "first_name" field.
    The legal company name is recorded in the "last_name" field.
    The "first_name" and "last_name" fields are taken from the "user" field.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer', blank=True, null=True) # blank=True, null=True will delete
    no = models.IntegerField(blank=True, null=True)
    sector = models.CharField(max_length=200, blank=True, null=True)
    organization_type = models.CharField(max_length=200, blank=True, null=True)
    organization_ownership = models.CharField(max_length=200, blank=True, null=True)
    number_of_employees = models.CharField(max_length=15, blank=True, null=True)
    second_email = models.EmailField(blank=True, null=True)
    other_email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    slider = models.BooleanField(default=False, null=True)

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate')
    id_card_number = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    birthday = models.DateField(null=True)
    citizenship = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)

    def __str__(self) -> str:
        return self.user.get_full_name()