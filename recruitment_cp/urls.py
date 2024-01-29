from django.urls import path

from recruitment_cp.views import main, parameters

app_name = 'cp'

urlpatterns = [
    path('', main.index, name='cp-index'),

    #PARAMETER URLS
    path('parameters/career-type', parameters.career_type_index, name='career_type'),
    path('parameters/career-type-load', parameters.career_type_load, name='career_type_load'),
    path('parameters/career-type-save', parameters.career_type_save, name='career_type_save'),

    path('parameters/career-level', parameters.career_level_index, name='career_level'),
    path('parameters/career-level-load', parameters.career_level_load, name='career_level_load'),
    path('parameters/career-level-save', parameters.career_level_save, name='career_level_save'),

    path('parameters/career-type-and-level', parameters.career_type_level_index, name='career_type_level'),
    path('parameters/career-type-and-level-load', parameters.career_type_level_load, name='career_type_level_load'),
    path('parameters/career-type-and-level-save', parameters.career_type_level_save, name='career_type_level_save'),

    path('parameters/location', parameters.location_index, name='location'),
    path('parameters/location-load', parameters.location_load, name='location_load'),
    path('parameters/location-save', parameters.location_save, name='location_save'),

    path('parameters/fte', parameters.fte_index, name='fte'),
    path('parameters/fte-load', parameters.fte_load, name='fte_load'),
    path('parameters/fte-save', parameters.fte_save, name='fte_save'),

    path('parameters/job-catalogue', parameters.job_catalogue_index, name='job_catalogue'),
    path('parameters/job-catalogue-load', parameters.job_catalogue_load, name='job_catalogue_load'),
    path('parameters/job-catalogue-save', parameters.job_catalogue_save, name='job_catalogue_save'),

    path('parameters/employee-type', parameters.employee_type_index, name='employee_type'),
    path('parameters/employee-type-load', parameters.employee_type_load, name='employee_type_load'),
    path('parameters/employee-type-save', parameters.employee_type_save, name='employee_type_save'),

    path('parameters/vacancy', parameters.vacancy_index, name='vacancy'),
    path('parameters/vacancy-load', parameters.vacancy_load, name='vacancy_load'),
    path('parameters/vacancy-save', parameters.vacancy_save, name='vacancy_save'),
]