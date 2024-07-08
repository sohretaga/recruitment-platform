from django import forms

from job.models import Vacancy
from blog.models import Blog
from user.models import Employer, Candidate
from main.models import FAQ

class PostVacancyForm(forms.ModelForm):
    definition = forms.CharField(widget=forms.Textarea, required=False)
    salary = forms.IntegerField(required=False)
    salary_minimum = forms.IntegerField(required=False)
    salary_midpoint = forms.IntegerField(required=False)
    salary_maximum = forms.IntegerField(required=False)
    keywords = forms.JSONField(required=False)
    
    class Meta:
        model = Vacancy
        fields = ('language', 'career_type', 'career_level', 'location', 'fte', 'salary', 'salary_minimum', 'salary_midpoint', 'salary_maximum',
                  'position_title', 'job_title', 'employment_type', 'definition', 'work_preference', 'department', 'status', 'keywords')

class PostBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'cover_photo', 'content', 'quick_career_tip', 'status')

class ManageEmployerAccountForm(forms.ModelForm):
    primary_email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=False)
    whatsapp = forms.CharField(max_length=15 ,required=False)
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
    whatsapp = forms.CharField(max_length=15, required=False)
    linkedin_url = forms.URLField(required=False)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Candidate
        exclude = ['id', 'user']

class ManageFaqForm(forms.ModelForm):

    class Meta:
        model = FAQ
        fields = "__all__"