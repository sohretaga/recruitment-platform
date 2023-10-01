from django.urls import path

from recruitment_cp.views import main, parameters

app_name = 'cp'

urlpatterns = [
    path('', main.index, name='cp-index'),

    #PARAMETER URLS
    path('parameters/career-type', parameters.career_type_index, name='career_type'),

    path('parameters/career-level', parameters.career_level_index, name='career_level'),

    path('parameters/career-type-and-level', parameters.career_type_level_index, name='career_type_level'),

    path('parameters/location', parameters.location, name='location'),

    path('parameters/fte', parameters.fte, name='fte'),

    path('parameters/job-catalogue', parameters.job_catalogue, name='job_catalogue')
]