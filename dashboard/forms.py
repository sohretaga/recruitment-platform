from django import forms

from recruitment_cp.models import ParameterVacancy
from blog.models import Blog

class CompleteEmployerRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company_name = forms.CharField(max_length=100)

class CompleteCandidateRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

class PostVacancyForm(forms.ModelForm):
    class Meta:
        model = ParameterVacancy
        fields = ('language', 'organization', 'career_type', 'career_level', 'location', 'fte', 'salary_minimum',
                  'salary_midpoint', 'salary_maximum', 'position_title', 'job_title', 'employment_type', 'definition')

class PostBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'cover_photo', 'content')