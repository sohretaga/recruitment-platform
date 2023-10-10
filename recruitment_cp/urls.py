from django.urls import path

from recruitment_cp.views import main, parameters

app_name = 'cp'

urlpatterns = [
    path('', main.index, name='cp-index'),

    #PARAMETER URLS
    path('parameters/career-type', parameters.pm_career_type_index, name='career_type'),
    path('parameters/career-type-load', parameters.pm_career_type_load, name='career_type_load'),
    path('parameters/career-type-save', parameters.pm_career_type_save, name='career_type_save'),

    path('parameters/career-level', parameters.pm_career_level_index, name='career_level'),
    path('parameters/career-level-load', parameters.pm_career_level_load, name='career_level_load'),
    path('parameters/career-level-save', parameters.pm_career_level_save, name='career_level_save'),

    path('parameters/career-type-and-level', parameters.pm_career_type_level_index, name='career_type_level'),
    path('parameters/career-type-and-level-load', parameters.pm_career_type_level_load, name='career_type_level_load'),
    path('parameters/career-type-and-level-save', parameters.pm_career_type_level_save, name='career_type_level_save'),

    path('parameters/location', parameters.pm_location_index, name='location'),
    path('parameters/location-load', parameters.pm_location_load, name='location_load'),
    path('parameters/location-save', parameters.pm_location_save, name='location_save'),

    path('parameters/fte', parameters.pm_fte_index, name='fte'),
    path('parameters/fte-load', parameters.pm_fte_load, name='fte_load'),
    path('parameters/fte-save', parameters.pm_fte_save, name='fte_save'),

    path('parameters/job-catalogue', parameters.pm_job_catalogue_index, name='job_catalogue'),
    path('parameters/job-catalogue-load', parameters.pm_job_catalogue_load, name='job_catalogue_load'),
    path('parameters/job-catalogue-save', parameters.pm_job_catalogue_save, name='job_catalogue_save')
]