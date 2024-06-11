from django import forms

from job.models import Vacancy
from blog.models import Blog
from user.models import Employer, Candidate

class CompleteEmployerRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company_name = forms.CharField(max_length=100)

class CompleteCandidateRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

class PostVacancyForm(forms.ModelForm):
    definition = forms.CharField(widget=forms.Textarea, required=False)
    salary = forms.IntegerField(required=False)
    salary_minimum = forms.IntegerField(required=False)
    salary_midpoint = forms.IntegerField(required=False)
    salary_maximum = forms.IntegerField(required=False)
    
    class Meta:
        model = Vacancy
        fields = ('language', 'career_type', 'career_level', 'location', 'fte', 'salary', 'salary_minimum', 'salary_midpoint', 'salary_maximum',
                  'position_title', 'job_title', 'employment_type', 'definition', 'work_preference', 'department', 'status', 'keywords')

class PostBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'cover_photo', 'content', 'status')


class EditEmployerAccountForm(forms.ModelForm):
    primary_email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = Employer
        exclude = ['id', 'no', 'user']