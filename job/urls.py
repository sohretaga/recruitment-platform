from django.urls import path
from job import views

app_name = 'job'

urlpatterns = [
    path('vacancies/', views.vacancies, name='vacancies'),
    path('vacancy/<slug:slug>', views.vacancy, name='vacancy'),
    path('vacancy/applicants/<slug:slug>', views.vacancy_applications, name='applicants'),
    path('categories', views.categories, name='categories'),
    path('applications', views.applications, name='applications'),
    path('job-postings', views.job_postings, name='job-postings'),
    path('bookmarks', views.bookmarks, name='bookmarks'),

    # ajax
    path('ajax/filter-vacancies', views.ajax_filter_vacancies, name='ajax_filter_vacancies'),
    path('ajax/add-bookmark', views.ajax_add_bookmark, name='ajax-add-bookmark'),
    path('ajax/apply', views.ajax_apply, name='ajax-apply'),
    path('ajax/send-employer-action', views.ajax_send_employer_action, name='ajax-send-employer-action'),
    path('ajax/send-candidate-action', views.ajax_send_candidate_action, name='ajax-send-candidate-action'),
    path('ajax/search-vacancy', views.ajax_search_vacancy, name='ajax-search-vacancy'),
    path('ajax/ajax-filter-job-postings', views.ajax_filter_job_postings, name='ajax-filter-job-postings'),
]