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
    path('notifications', views.notifications, name='notifications'),

    #AJAX
    path('ajax/get-notifications', views.get_notifications, name='ajax-get-notifications'),
    path('ajax/delete-notifications', views.delete_notifications, name='ajax-delete-notifications'),
    path('ajax/delete-notification', views.delete_notification, name='ajax-delete-notifications'),
]