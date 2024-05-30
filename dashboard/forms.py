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
        fields = ('language', 'author', 'organization', 'career_type', 'career_level', 'location', 'fte', 'salary', 'salary_minimum',
                  'salary_midpoint', 'salary_maximum', 'position_title', 'job_title', 'employment_type', 'definition')

class EditVacancyForm(forms.ModelForm):
    definition = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = ParameterVacancy
        fields = ('language', 'career_type', 'career_level', 'location', 'fte', 'salary', 'salary_minimum',
                  'salary_midpoint', 'salary_maximum', 'position_title', 'job_title', 'employment_type', 'definition')

class PostBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'cover_photo', 'content', 'status')