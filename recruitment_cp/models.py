from django.db import models
from django.db.models import F, Value, CharField, When, Case
from django.core.cache import cache
from django.conf import settings

# Create your models here.

class SiteContent(models.Model):
    PAGE_CHOICES = (
        ('SIGN_UP', 'Sign Up'),
        ('SIGN_IN', 'Sign In'),
        ('SIGN_OUT', 'Sign Out'),
        ('CONTACT', 'Contact'),
        ('CONTACT_THANKS_MESSAGE', 'Contact - Thanks Message'),
        ('TERMS', 'Privacy & Policy'),
        ('EMPLOYER_COMPLETE_REGISTER', 'Employer - Complete Register'),
        ('CANDIDATE_COMPLETE_REGISTER', 'Candidate - Complete Register'),
        ('HOW_IT_WORK', 'How It Work'),
        ('SERVICES', 'Services'),
        ('HOME', 'Home'),
        ('TEAM', 'Team'),
        ('QUICK_CAREER_TIPS', 'Quick Career Tips'),
        ('SUBSCRIBE', 'Subscribe'),
        ('RESET_PASSWORD', 'Reset Password')
    )

    page = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title EN')
    title_tr = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title TR')

    content = models.TextField(blank=True, null=True, verbose_name='Content EN')
    content_tr = models.TextField(blank=True, null=True, verbose_name='Content TR')

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

class ParameterCommonFieldsQuerySet(models.QuerySet):
    def custom_update(self, language, **kwargs):
        match language:
            case 'en':
                if 'name' in kwargs:
                    kwargs['name_en'] = kwargs.pop('name')
                if 'definition' in kwargs:
                    kwargs['definition_en'] = kwargs.pop('definition')
                if 'note' in kwargs:
                    kwargs['note_en'] = kwargs.pop('note')

            case 'tr':
                if 'name' in kwargs:
                    kwargs['name_tr'] = kwargs.pop('name')
                if 'definition' in kwargs:
                    kwargs['definition_tr'] = kwargs.pop('definition')
                if 'note' in kwargs:
                    kwargs['note_tr'] = kwargs.pop('note')

        return super().update(**kwargs)

class ParameterCommonFieldsManager(models.Manager):
    def get_queryset(self):
        return ParameterCommonFieldsQuerySet(self.model, using=self._db)

class ParameterCommonFields(models.Model):
    no = models.IntegerField(blank=True, null=True)
    name_en = models.CharField(max_length=500)
    name_tr = models.CharField(max_length=500, blank=True, null=True)

    definition_en = models.TextField(blank=True, null=True)
    definition_tr = models.TextField(blank=True, null=True)

    note_en = models.CharField(max_length=500, blank=True, null=True)
    note_tr = models.CharField(max_length=500, blank=True, null=True)

    objects = ParameterCommonFieldsManager()

    class Meta:
        abstract = True
        ordering = ['no']

    def save(self, language, *args, **kwargs):

        if 'no' in kwargs:
            self.no = kwargs['no']

        match language:
            case 'en':
                if 'name' in kwargs:
                    self.name_en = kwargs['name']
                if 'definition' in kwargs:
                    self.definition_en = kwargs['definition']
                if 'note' in kwargs:
                    self.note_en = kwargs['note']

            case 'tr':
                if 'name' in kwargs:
                    self.name_tr = kwargs['name']
                if 'definition' in kwargs:
                    self.definition_tr = kwargs['definition']
                if 'note' in kwargs:
                    self.note_tr = kwargs['note']

        super().save()

    @classmethod
    def translation(cls):
        language = cache.get('site_language', settings.SITE_LANGUAGE_CODE)
        match language:
            case 'en':
                objects = cls.objects.annotate(
                    name = F('name_en'),
                )
            case 'tr':
                objects = cls.objects.annotate(
                    name = Case(
                         When(name_tr__isnull=False, then=F('name_tr')),
                         default=F('name_en'),
                         output_field=CharField()
                    )
                )

        return objects
    
    @classmethod
    def language_filter(cls, language_code):
        match language_code:
            case 'en':
                objects = cls.objects.annotate(
                    name = F('name_en'),
                    definition = F('definition_en'),
                    note = F('note_en')
                )
            case 'tr':
                objects = cls.objects.annotate(
                    name = F('name_tr'),
                    definition = F('definition_tr'),
                    note = F('note_tr')
                )
            case _:
                objects = cls.objects.annotate(
                    name = Value(value='', output_field=CharField()),
                    definition = Value(value='', output_field=CharField()),
                    note = Value(value='', output_field=CharField())
                )
        return objects

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
    trending = models.BooleanField(default=False)

class ParameterFAQ(ParameterCommonFields):
    ...

class ParameterCompetence(ParameterCommonFields):
    ...

class ParameterJobFamily(ParameterCommonFields):
    ...

class ParameterDatePosted(ParameterCommonFields):
    hours = models.PositiveIntegerField()