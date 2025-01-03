from django import forms

from job.models import Vacancy
from blog.models import Blog
from user.models import Employer, Candidate
from main.models import FAQ

class PostVacancyForm(forms.ModelForm):
    salary = forms.IntegerField()
    salary_minimum = forms.IntegerField()
    salary_maximum = forms.IntegerField()
    keywords = forms.JSONField()
    
    class Meta:
        model = Vacancy
        fields = (
            'language', 'career_type', 'career_level', 'location', 'fte', 'salary',
            'salary_minimum', 'salary_maximum', 'position_title', 'job_title',
            'employment_type', 'work_preference', 'department', 'status', 'keywords',
            'description', 'responsibilities', 'qualification', 'skill_experience', 'additional', 'anonium'
        )

class PostBlogForm(forms.ModelForm):
    language = forms.CharField(max_length=2)

    class Meta:
        model = Blog
        exclude = ['id', 'views', 'slug', 'created_date']

class ManageEmployerAccountForm(forms.ModelForm):
    primary_email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=False)
    establishment_date = forms.DateField(required=False)
    website = forms.URLField(required=False)
    whatsapp = forms.CharField(max_length=15, required=False)
    linkedin_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Employer
        exclude = ['id', 'no', 'user']

class ManageCandidateAccountForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15 ,required=True)
    address = forms.CharField(max_length=255, required=False)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    languages = forms.CharField(max_length=255, required=False)
    functionals = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Candidate
        exclude = ['id', 'user', 'views']

class ManageFaqForm(forms.ModelForm):

    class Meta:
        model = FAQ
        fields = "__all__"