from django.urls import path
from recruitment_main.views import main

urlpatterns = [
    path('', main.index, name='main-index')
]