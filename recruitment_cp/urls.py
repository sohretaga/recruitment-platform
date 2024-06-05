from django.urls import path

from recruitment_cp.views import main, parameters

app_name = 'cp'

urlpatterns = [
    path('', main.index, name='cp-index'),

    path('load-source', main.load_source, name='load_source'),

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

    path('parameters/country', parameters.country_index, name='country'),
    path('parameters/country-load', parameters.country_load, name='country_load'),
    path('parameters/country-save', parameters.country_save, name='country_save'),

    path('parameters/location', parameters.location_index, name='location'),
    path('parameters/location-load', parameters.location_load, name='location_load'),
    path('parameters/location-save', parameters.location_save, name='location_save'),

    path('parameters/work-experience', parameters.work_experience_index, name='work_experience'),
    path('parameters/work-experience-load', parameters.work_experience_load, name='work_experience_load'),
    path('parameters/work-experience-save', parameters.work_experience_save, name='work_experience_save'),

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
    path('parameters/vacancy-lazy-load', parameters.ajax_vacancy_load, name='ajax_vacancy_load'),

    path('parameters/blog-category', parameters.blog_category_index, name='blog_category'),
    path('parameters/blog-category-load', parameters.blog_category_load, name='blog_category_load'),
    path('parameters/blog-category-save', parameters.blog_category_save, name='blog_category_save'),

    path('parameters/company', parameters.company_index, name='company'),
    path('parameters/company-load', parameters.company_load, name='company_load'),
    path('parameters/company-save', parameters.company_save, name='company_save'),

    path('parameters/sector', parameters.sector_index, name='sector'),
    path('parameters/sector-load', parameters.sector_load, name='sector_load'),
    path('parameters/sector-save', parameters.sector_save, name='sector_save'),

    path('parameters/organization-type', parameters.organization_type_index, name='organization_type'),
    path('parameters/organization-type-load', parameters.organization_type_load, name='organization_type_load'),
    path('parameters/organization-type-save', parameters.organization_type_save, name='organization_type_save'),

    path('parameters/organization-ownership', parameters.organization_ownership_index, name='organization_ownership'),
    path('parameters/organization-ownership-load', parameters.organization_ownership_load, name='organization_ownership_load'),
    path('parameters/organization-ownership-save', parameters.organization_ownership_save, name='organization_ownership_save'),

    path('parameters/number-of-employees', parameters.number_of_employees_index, name='number_of_employees'),
    path('parameters/number-of-employees-load', parameters.number_of_employees_load, name='number_of_employees_load'),
    path('parameters/number-of-employees-save', parameters.number_of_employees_save, name='number_of_employees_save'),

    path('parameters/department', parameters.department_index, name='department'),
    path('parameters/department-load', parameters.department_load, name='department_load'),
    path('parameters/department-save', parameters.department_save, name='department_save'),

    path('parameters/work-preference', parameters.work_preference_index, name='work_preference'),
    path('parameters/work-preference-load', parameters.work_preference_load, name='work_preference_load'),
    path('parameters/work-preference-save', parameters.work_preference_save, name='work_preference_save'),
]