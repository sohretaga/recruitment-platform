from django.db import models
from django.db.models import F, Value, CharField, When, Case
from django.core.cache import cache
from language.utils import get_cache_key
from language.middleware import get_current_user_language

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
        ('RESET_PASSWORD', 'Reset Password'),
        ('CONFIRM_PASSWORD_RESET', 'Confirm Password Reset'),
        ('CONFIRM_VACANCY', 'Confirm Vacancy - DASHBOARD'),
        ('PAYMENT_MODAL', 'Payment Modal - DASHBOARD')
    )

    page = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)

    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title EN')
    title_tr = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title TR')

    content_en = models.TextField(blank=True, null=True, verbose_name='Content EN')
    content_tr = models.TextField(blank=True, null=True, verbose_name='Content TR')

    image = models.ImageField(upload_to='site-content/', blank=True, null=True)

    def short_content(self) -> str:
        return self.content_en[:75]+'...' if len(self.content_en) > 75 else self.content_en

    short_content.short_description = 'Content'

    def __str__(self) -> str:
        return self.page
    
    def save(self, *args, **kwargs) -> None:
        cache.set(get_cache_key(f'title_{self.page}', 'en'), self.title_en, timeout=None)
        cache.set(get_cache_key(f'title_{self.page}', 'tr'), self.title_tr, timeout=None)

        cache.set(get_cache_key(f'content_{self.page}', 'en'), self.content_en, timeout=None)
        cache.set(get_cache_key(f'content_{self.page}', 'tr'), self.content_tr, timeout=None)

        cache.set(get_cache_key(f'image_{self.page}', ''), self.image, timeout=None)

        super(SiteContent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Site Content'
        verbose_name_plural = 'Site Contents'

    @classmethod
    def translation(cls):
        language = get_current_user_language()
        objects = cls.objects.annotate(
            title = Case(
                When(**{f'title_{language}__isnull':False}, then=F(f'title_{language}')),
                default=F('title_en'),
                output_field=CharField()
            ),
            content = Case(
                When(**{f'content_{language}__isnull':False}, then=F(f'content_{language}')),
                default=F('content_en'),
                output_field=CharField()
            )
        )
        return objects

class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    is_default = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def save(self,*args, **kwargs) -> None:
        self.code = self.code.lower()
        super().save(*args, **kwargs)

class ParameterCommonFieldsQuerySet(models.QuerySet):
    def custom_update(self, language, *args, **kwargs):
        if 'name' in kwargs:
            kwargs[f'name_{language}'] = kwargs.pop('name')
        if 'definition' in kwargs:
            kwargs[f'definition_{language}'] = kwargs.pop('definition')
        if 'note' in kwargs:
            kwargs[f'note_{language}'] = kwargs.pop('note')

        super().update(*args, **kwargs)

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
        language = get_current_user_language()
        objects = cls.objects.annotate(
            name = Case(
                    When(**{f'name_{language}__isnull':False}, then=F(f'name_{language}')),
                    default=F('name_en'),
                    output_field=CharField()
            )
        )
        return objects
    
    @classmethod
    def language_filter(cls, language_code):
        objects = cls.objects.annotate(
            name = Case(
                When(**{f'name_{language_code}__isnull':False},
                     then=F(f'name_{language_code}')),
                     default=Value(''),
                     output_field=CharField()
            ),

            definition = Case(
                When(**{f'definition_{language_code}__isnull':False},
                     then=F(f'definition_{language_code}')),
                     default=Value(''),
                     output_field=CharField()
            ),

            note = Case(
                When(**{f'note_{language_code}__isnull':False},
                     then=F(f'note_{language_code}')),
                     default=Value(''),
                     output_field=CharField()
            )
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
    minimum = models.FloatField()
    maximum = models.FloatField()

class ParameterFTE(ParameterCommonFields):
    ...

class ParameterJobFamily(ParameterCommonFields):
    ...

class ParameterEducationLevel(ParameterCommonFields):
    level_order = models.PositiveIntegerField()

class ParameterJobCatalogue(ParameterCommonFields):
    """
    - Job Title is name field
    - Common Duties and Responsibilities is definition field
    """

    job_family = models.ForeignKey(ParameterJobFamily, on_delete=models.SET_NULL, blank=True, null=True)
    job_sub_family = models.CharField(max_length=100, blank=True, null=True)
    career_type = models.ForeignKey(ParameterCareerType, on_delete=models.SET_NULL, blank=True, null=True)
    career_level = models.CharField(max_length=100, blank=True, null=True)
    typical_education = models.ForeignKey(ParameterEducationLevel, on_delete=models.SET_NULL, blank=True, null=True)
    relevant_experience = models.ForeignKey(ParameterWorkExperience, on_delete=models.SET_NULL, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    skill_experience = models.TextField(blank=True, null=True)

    job_code = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def language_filter(cls, language_code):
        objects = super().language_filter(language_code)

        objects = objects.annotate(
            job_family_name = F(f'job_family__name_{language_code}'),
            career_type_name = F(f'career_type__name_{language_code}'),
            typical_education_name = F(f'typical_education__name_{language_code}'),
            relevant_experience_name = F(f'relevant_experience__name_{language_code}')
        )

        return objects

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

class ParameterCompetenceGrouping(ParameterCommonFields):
    ...

class ParameterCompetence(ParameterCommonFields):
    grouping = models.ForeignKey(ParameterCompetenceGrouping, on_delete=models.SET_NULL, null=True, blank=True)
    behavioral_competence = models.CharField(max_length=150, null=True, blank=True)
    functional_competence = models.CharField(max_length=150, null=True, blank=True)
    it_competence = models.CharField(max_length=150, null=True, blank=True)
    language_competence = models.CharField(max_length=150, null=True, blank=True)

    @classmethod
    def language_filter(cls, language_code):
        objects = super().language_filter(language_code)

        objects = objects.annotate(
            grouping_name = Case(
                When(**{f'grouping__name_{language_code}__isnull':False},
                     then=F(f'grouping__name_{language_code}')),
                     default=Value(''),
                     output_field=CharField()
            ),
        )

        return objects

class ParameterDatePosted(ParameterCommonFields):
    hours = models.PositiveIntegerField()

class ParameterAgeGroup(ParameterCommonFields):
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()

class ParameterPricing(ParameterCommonFields):
    definition_en = None
    definition_tr = None
    note_en = None
    note_tr = None

    # category field is name field
    standard = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    hot_vacancies = models.PositiveIntegerField()
    active = models.BooleanField(default=False)

    @classmethod
    def language_filter(cls, language_code):
        objects = cls.objects.annotate(
            name = Case(
                When(**{f'name_{language_code}__isnull':False},
                     then=F(f'name_{language_code}')),
                     default=Value(''),
                     output_field=CharField()
            ),
        )
        return objects