from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='main-index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('team', views.team, name='team'),
    path('pricing', views.pricing, name='pricing'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('faqs', views.faqs, name='faqs'),
    path('coming-soon', views.coming_soon, name='coming-soon'),
    path('get-notifications', views.get_notifications, name='get-notifications'),
    path('notifications', views.notifications, name='notifications'),
]