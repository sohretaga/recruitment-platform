from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('sign-in', views.sign_in, name='sign-in'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-out', views.sign_out, name='sign-out'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('profile', views.profile, name='profile')
]