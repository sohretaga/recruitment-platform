from django.urls import path
from recruitment_main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='main-index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about')
]