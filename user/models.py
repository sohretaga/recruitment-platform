from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F, Case, When, Value, CharField, Subquery, OuterRef, FloatField
from django.db.models.functions import ExtractYear
from django.core.validators import MinLengthValidator, MaxLengthValidator
from datetime import datetime

from recruitment_cp.models import (
    ParameterSector,
    ParameterOrganizationType,
    ParameterOrganizationOwnership,
    ParameterNumberOfEmployee,
    ParameterCountry,
    ParameterAgeGroup,
    ParameterWorkExperience,
    ParameterEducationLevel,
    ParameterCareerType,
    ParameterLocation,
    ParameterEmployeeType,
    ParameterJobCatalogue,
    ParameterCompetence
)
from .utils import calculate_recent_duration
from language.middleware import get_current_user_language

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
        ('blogger', 'Content'),
        ('controller', 'Controller'),
    )

    username = models.CharField(
        max_length=19,
        unique=True,
        validators=[
            MinLengthValidator(2, message='Username must be at least 2 characters long.'),
        ],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    profile_photo = models.ImageField(upload_to='profile-photos/', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    about = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
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
    background_image = models.ImageField(upload_to='background-images/', null=True, blank=True)
    no = models.IntegerField(blank=True, null=True)

    sector = models.ForeignKey(ParameterSector, on_delete=models.SET_NULL, blank=True, null=True)
    organization_type = models.ForeignKey(ParameterOrganizationType, on_delete=models.SET_NULL, blank=True, null=True)
    organization_ownership = models.ForeignKey(ParameterOrganizationOwnership, on_delete=models.SET_NULL, blank=True, null=True)
    number_of_employees = models.ForeignKey(ParameterNumberOfEmployee, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(ParameterCountry, on_delete=models.SET_NULL, blank=True, null=True)

    second_email = models.EmailField(blank=True, null=True)
    other_email = models.EmailField(blank=True, null=True)
    certificate_of_registration = models.FileField(upload_to='certificates/', blank=True, null=True) 
    note = models.TextField(blank=True, null=True)
    slider = models.BooleanField(default=False, null=True)
    establishment_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    discount_code = models.CharField(max_length=6, blank=True, null=True)
    amcham_user = models.BooleanField(default=False)
    key_account = models.BooleanField(default=False)

    @classmethod
    def translation(cls):
        language = get_current_user_language()

        employers = cls.objects.annotate(
            sector_name=F(f'sector__name_{language}'),
            organization_type_name=F(f'organization_type__name_{language}'),
            organization_ownership_name=F(f'organization_ownership__name_{language}'),
            number_of_employees_name=F(f'number_of_employees__name_{language}'),
            location_name=F(f'location__name_{language}'),
        )

        return employers

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate')
    id_card_number = models.CharField(max_length=20, null=True)
    birthday = models.DateField(null=True)
    languages = models.ManyToManyField(ParameterCompetence, blank=True, related_name='candidate_languages')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    citizenship = models.ForeignKey(ParameterCountry, on_delete=models.SET_NULL, null=True)
    occupation = models.ForeignKey(ParameterJobCatalogue, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.user.get_full_name()
    
    @classmethod
    def translation(cls):
        language = get_current_user_language()
        current_year = datetime.now().year
        age_groups = ParameterAgeGroup.translation().values('minimum', 'maximum', 'name')
        work_experiences = ParameterWorkExperience.translation().values('minimum', 'maximum', 'name')
        latest_experience = calculate_recent_duration(Experience)

        education_level_case = Education.translation().filter(
            candidate=OuterRef('pk')
        ).order_by('-education_level__level_order').values('education_level_name')[:1]

        age_group_cases = [
            When(
                age__gte=age_group.get('minimum'),
                age__lte=age_group.get('maximum'),
                then=Value(age_group.get('name'))
            )
            for age_group in age_groups
        ]

        work_experience_case = [
            When(
                experience_duration_years__gte=experience.get('minimum'),
                experience_duration_years__lte=experience.get('maximum'),
                then=Value(experience.get('name'))
            )
            for experience in work_experiences
        ]

        candidates = cls.objects.annotate(
            age=current_year-ExtractYear(F('birthday')),
            age_group=Case(
                *age_group_cases,
                default=Value(''),
                output_field=CharField()
            ),
            citizenship_name=Case(
                When(**{f'citizenship__name_{language}__isnull':False},
                     then=F(f'citizenship__name_{language}')),
                     default=Value(''),
                     output_field=CharField()
            ),
            experience_duration_years=Subquery(latest_experience, output_field=FloatField()),
            work_experience_name=Case(
                *work_experience_case,
                default=Value(''),
                output_field=CharField()
            ),
            education_level_name=Subquery(
                education_level_case,
                output_field=CharField(),
            ),
            occupation_name=F(f'occupation__name_{language}'),
            job_family = F(f'occupation__job_family__name_{language}')
        )

        return candidates

class Gallery(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='gallery')

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Education(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=255)
    speciality = models.CharField(max_length=500)
    education_level = models.ForeignKey(ParameterEducationLevel, on_delete=models.SET_NULL, null=True)

    start_date_month = models.CharField(max_length=15)
    start_date_year = models.IntegerField()

    end_date_month = models.CharField(max_length=15)
    end_date_year = models.IntegerField()

    description = models.TextField()

    @classmethod
    def translation(cls):
        language = get_current_user_language()
        educations = cls.objects.annotate(
            education_level_name=Case(
                When(**{f'education_level__name_{language}__isnull':False},
                     then=F(f'education_level__name_{language}')
                ),
                default=Value(''),
                output_field=CharField()
            )
        )
        return educations

class Experience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=500)

    start_date_month = models.CharField(max_length=15)
    start_date_year = models.IntegerField()

    end_date_month = models.CharField(max_length=15, blank=True, null=True)
    end_date_year = models.IntegerField(blank=True, null=True)

    present = models.BooleanField()
    description = models.TextField()

class Project(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='projects')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=500)

    start_date_month = models.CharField(max_length=15)
    start_date_year = models.IntegerField()

    end_date_month = models.CharField(max_length=15, blank=True, null=True)
    end_date_year = models.IntegerField(blank=True, null=True)

    present = models.BooleanField()
    description = models.TextField()

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')

class CandidateBookmark(models.Model):
    # Employers bookmark candidates
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='bookmarks')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

class CandidatePreference(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name='preference')
    companies = models.ManyToManyField(Employer, blank=True, related_name='preferred_employers')
    career_types = models.ManyToManyField(ParameterCareerType, blank=True, related_name='preferred_career_types')
    locations = models.ManyToManyField(ParameterLocation, blank=True, related_name='preferred_locations')
    types_of_employment = models.ManyToManyField(ParameterEmployeeType, blank=True, related_name='preferred_employment_types')
    min_salary = models.PositiveIntegerField(null=True, blank=True)
    max_salary = models.PositiveIntegerField(null=True, blank=True)

    @property
    def offered_salary(self):
        if self.min_salary and self.max_salary:
            return int((int(self.min_salary) + int(self.max_salary)) / 2)
        else:
            return False