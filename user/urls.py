from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('sign-in', views.sign_in, name='sign-in'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-out', views.sign_out, name='sign-out'),
    path('reset-password', views.reset_password, name='reset-password'),

    path('profile', views.profile, name='profile'),
    path('gallery-upload', views.gallery_upload, name='gallery-upload'),
    path('ajax-delete-gallery-image', views.delete_gallery_image, name='ajax-delete-gallery-image'),

    path('candidate-list', views.candidate_list, name='candidate-list'),
    path('candidate/<str:username>', views.candidate_details, name='candidate'),

    path('company-list', views.company_list, name='company-list'),
    path('company/<str:username>', views.company_details, name='company')
]