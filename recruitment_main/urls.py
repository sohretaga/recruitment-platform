from django.urls import path
from recruitment_main.views import main

app_name = 'main'

urlpatterns = [
    path('', main.index, name='main-index'),
    path('vacancy/load', main.vacancy_load, name='vacancy-load'),
]