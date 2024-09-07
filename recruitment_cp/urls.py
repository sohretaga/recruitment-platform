from django.urls import path

from recruitment_cp.views import main, parameters, languages

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

    path('parameters/blog-category', parameters.blog_category_index, name='blog_category'),
    path('parameters/blog-category-load', parameters.blog_category_load, name='blog_category_load'),
    path('parameters/blog-category-save', parameters.blog_category_save, name='blog_category_save'),

    path('parameters/company', parameters.company_index, name='company'),
    path('parameters/company-load', parameters.company_load, name='company_load'),
    path('parameters/company-save', parameters.company_save, name='company_save'),
    path('parameters/ajax/generate-discount-code', parameters.generate_discount_code, name='generate_discount_code'),

    path('parameters/candidate', parameters.candidate_index, name='candidate'),
    path('parameters/candidate-load', parameters.candidate_load, name='candidate_load'),
    path('parameters/candidate-save', parameters.candidate_save, name='candidate_save'),

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

    path('parameters/keywords', parameters.keywords_index, name='keywords'),
    path('parameters/keywords-load', parameters.keywords_load, name='keywords_load'),
    path('parameters/keywords-save', parameters.keywords_save, name='keywords_save'),

    path('parameters/faq-categories', parameters.faq_index, name='faq_categories'),
    path('parameters/faq-categories-load', parameters.faq_load, name='faq_categories_load'),
    path('parameters/faq-categories-save', parameters.faq_save, name='faq_categories_save'),

    path('parameters/competence', parameters.competence_index, name='competence'),
    path('parameters/competence-load', parameters.competence_load, name='competence_load'),
    path('parameters/competence-save', parameters.competence_save, name='competence_save'),

    path('parameters/comp-grouping', parameters.competence_grouping_index, name='competence_grouping'),
    path('parameters/comp-grouping-load', parameters.competence_grouping_load, name='competence_grouping_load'),
    path('parameters/comp-grouping-save', parameters.competence_grouping_save, name='competence_grouping_save'),

    path('parameters/job-family', parameters.job_family_index, name='job_family'),
    path('parameters/job-family-load', parameters.job_family_load, name='job_family_load'),
    path('parameters/job-family-save', parameters.job_family_save, name='job_family_save'),

    path('parameters/date-posted', parameters.date_posted_index, name='date_posted'),
    path('parameters/date-posted-load', parameters.date_posted_load, name='date_posted_load'),
    path('parameters/date-posted-save', parameters.date_posted_save, name='date_posted_save'),

    path('parameters/age-group', parameters.age_group_index, name='age_group'),
    path('parameters/age-group-load', parameters.age_group_load, name='age_group_load'),
    path('parameters/age-group-save', parameters.age_group_save, name='age_group_save'),

    path('parameters/education-level', parameters.education_level_index, name='education_level'),
    path('parameters/education-level-load', parameters.education_level_load, name='education_level_load'),
    path('parameters/education-level-save', parameters.education_level_save, name='education_level_save'),

    #LANGUAGE URLS
    path('translation/contents', languages.contents, name='contents'),
    path('translation/contents-load', languages.contents_load, name='contents_load'),
    path('translation/contents-save', languages.contents_save, name='contents_save'),

    path('translation/languages', languages.languages, name='languages'),
    path('translation/languages-load', languages.languages_load, name='languages_load'),
    path('translation/languages-save', languages.languages_save, name='languages_save'),
]