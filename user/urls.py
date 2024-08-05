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

    path('candidate-list', views.candidate_list, name='candidate-list'),
    path('candidate/<str:username>', views.candidate_details, name='candidate'),

    path('company-list', views.company_list, name='company-list'),
    path('company/<str:username>', views.company_details, name='company'),

    path('manage-education', views.manage_education, name='manage-education'),

    path('manage-experience', views.manage_experience, name='manage-experience'),

    #AJAX
    path('ajax-delete-gallery-image', views.delete_gallery_image, name='ajax-delete-gallery-image'),
    path('ajax/delete-profile-image', views.delete_pfofile_image, name='delete-profile-image'),
    path('ajax/delete-education', views.delete_education, name='ajax-delete-education'),
    path('ajax/delete-experience', views.delete_experience, name='ajax-delete-experience'),
    path('ajax/add-candidate-bookmark', views.ajax_candidate_bookmarks, name='ajax-add-candidate-bookmark'),
]