from django.db import models

# Create your models here.

class SiteContent(models.Model):
    PAGE_CHOICES = (
        ('SIGN_UP', 'Sign Up'),
        ('SIGN_IN', 'Sign In'),
        ('SIGN_OUT', 'Sign Out'),
        ('CONTCAT', 'Contact'),
        ('TERMS', 'Privacy & Policy'),
        ('EMPLOYER_COMPLETE_REGISTER', 'Employer - Complete Register'),
        ('CANDIDATE_COMPLETE_REGISTER', 'Candidate - Complete Register'),
    )

    page = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='site-content/', blank=True, null=True)

    def short_content(self) -> str:
        return self.content[:75]+'...' if len(self.content) > 75 else self.content 
    
    short_content.short_description = 'Content'

    def __str__(self) -> str:
        return self.page
    
    class Meta:
        verbose_name = 'Site Content'
        verbose_name_plural = 'Site Contents'

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

class ParameterSector(ParameterCommonFields):
    ...

class ParameterOrganizationType(ParameterCommonFields):
    ...

class ParameterOrganizationOwnership(ParameterCommonFields):
    ...

class ParameterNumberOfEmployee(ParameterCommonFields):
    ...

class ParameterDepartment(ParameterCommonFields):
    ...

class ParameterWorkPreference(ParameterCommonFields):
    ...

class ParameterKeyword(ParameterCommonFields):
    ...

class ParameterFAQ(ParameterCommonFields):
    ...

class CompetenceFAQ(ParameterCommonFields):
    ...