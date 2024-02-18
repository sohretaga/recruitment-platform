from django.urls import path
from job import views

app_name = 'job'

urlpatterns = [
    path('vacancies', views.vacancies, name='vacancies'),
    path('vacancy', views.vacancy, name='vacancy'),
    path('categories', views.categories, name='categories'),
    path('manage-jobs', views.manage_jobs, name='manage-jobs'),
    path('bookmarks', views.bookmarks, name='bookmarks')
]