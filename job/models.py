from django.db import models
from django.utils.text import slugify
from django.db.models import F, Case, When, CharField, Value
from django.contrib.postgres.aggregates import ArrayAgg
from ckeditor.fields import RichTextField

from user.models import Employer, Candidate, CustomUser
from recruitment_cp import models as cp_models
from language.middleware import get_current_user_language

# Create your models here.

class BaseVacancy(models.Model):

    STATUS_CHOICES = [
        ('PUBLISHED', 'Published'),
        ('PENDING', 'Pending'),
        ('DEACTIVATED', 'Deactivated')
    ]

    TYPE_CHOICES = [
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium')
    ]

    no = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=5)

    position_title = models.CharField(max_length=500, blank=True, null=True)

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

    keywords = models.ManyToManyField(cp_models.ParameterKeyword, blank=True)
    delete = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    slug = models.SlugField(null=True)

    approval_level = models.CharField(max_length=12, choices=STATUS_CHOICES, default='PENDING')
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='STANDARD')
    status = models.BooleanField()
    anonium = models.BooleanField(default=False)

    description = RichTextField(blank=True, null=True)
    responsibilities = RichTextField(blank=True, null=True)
    qualification = RichTextField(blank=True, null=True)
    skill_experience = RichTextField(blank=True, null=True)
    additional = RichTextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    ending_date = models.DateTimeField(null=True)
    published_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created_date']
        abstract = True 

    def save(self, *args, **kwargs) -> None:
        if self.salary_minimum and self.salary_maximum:
            self.salary_midpoint = int((self.salary_minimum + self.salary_maximum) / 2)

        if not self.slug:
            self.slug = slugify(self.position_title)
            original_slug = self.slug
            queryset = self.__class__.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = self.__class__.objects.filter(slug=self.slug)
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.position_title
    
    @classmethod
    def translation(cls):
        language = get_current_user_language()
        vacancies = cls.objects.annotate(
            career_type_name = F(f'career_type__name_{language}'),
            career_level_name = F(f'career_level__name_{language}'),
            location_name = F(f'location__name_{language}'),
            fte_name = F(f'fte__name_{language}'),
            job_title_name = F(f'job_title__name_{language}'),
            employment_type_name = F(f'employment_type__name_{language}'),
            work_experience_name = F(f'work_experience__name_{language}'),
            work_preference_name = F(f'work_preference__name_{language}'),
            department_name = F(f'department__name_{language}'),
            employer_sector = F(f'employer__sector__name_{language}'),
            keywords_names=ArrayAgg(f'keywords__name_{language}', distinct=True)
        ).order_by('-created_date')

        return vacancies
    
    @classmethod
    def translation_for_filter(cls):
        """This method is used to perform operations only on the fields required
        for filtering, so that there are no unnecessary operations during filtering."""

        language = get_current_user_language()
        vacancies = cls.objects.annotate(
            location_name = F(f'location__name_{language}'),
            work_experience_name = F(f'work_experience__name_{language}'),
            employment_type_name = F(f'employment_type__name_{language}'),
            department_name = F(f'department__name_{language}'),
            work_preference_name = F(f'work_preference__name_{language}'),
            career_type_name = F(f'career_type__name_{language}'),
            job_title_name = F(f'job_title__name_{language}'),
            employer_sector = F(f'employer__sector__name_{language}'),
            keywords_names=ArrayAgg(f'keywords__name_{language}', distinct=True)
        ).order_by('-created_date')
        return vacancies

class Vacancy(BaseVacancy):
    employer = models.ForeignKey(Employer, related_name='vacancies', on_delete=models.CASCADE)

class ExpiredVacancy(BaseVacancy):
    employer = models.ForeignKey(Employer, related_name='expired_vacancies', on_delete=models.CASCADE)

class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    @classmethod
    def translation(cls):
        language = get_current_user_language()
        bookmarks = cls.objects.annotate(
            location=Case(
                When(**{f"vacancy__location__name_{language}__isnull":False},
                    then=F(f'vacancy__location__name_{language}')),
                    default=Value(''),
                    output_field=CharField()
            ),
            work_experience=Case(
                When(**{f"vacancy__work_experience__name_{language}__isnull": False},
                    then=F(f"vacancy__work_experience__name_{language}")),
                    default=Value(''),
                    output_field=CharField()
            )
        )

        return bookmarks

class Apply(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    cv = models.FileField(upload_to='cvs/', null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class EmployerAction(models.Model):
    # For translation, the same texts must be written in translation.html
    ACTION_CHOICES = [
        ('INVITE', 'The employer has invited you to an interview - NOTIFICATION'),
        ('SHORTLIST', 'The employer has shortlisted your application - NOTIFICATION'),
        ('DELIST', 'The employer has delisted your application - NOTIFICATION'),
        ('SUGGEST_OTHER_DATE', 'The employer has suggested another date - NOTIFICATION'),
        ('ACCEPT_REQUEST_OTHER_DATE', 'Accepted the request for another date - NOTIFICATION'),
    ]
    apply = models.OneToOneField(Apply, on_delete=models.CASCADE, related_name='employer_action')
    action = models.CharField(max_length=25, choices=ACTION_CHOICES)
    invite_date = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.action} on {self.apply}"


class CandidateAction(models.Model):
    # For translation, the same texts must be written in translation.html
    ACTION_CHOICES = [
        ('ACCEPT', 'Accepted your offer - NOTIFICATION'),
        ('REJECT', 'Rejected your offer - NOTIFICATION'),
        ('REQUEST_OTHER_DATE', 'Requested another date - NOTIFICATION'),
    ]
    apply = models.OneToOneField(Apply, on_delete=models.CASCADE, related_name='candidate_action')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    request_other_date = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.action} for {self.employer_action}"