from django.urls import path

from recruitment_cp.views import main

urlpatterns = [
    path('', main.index, name='cp-index')
]