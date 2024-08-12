from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:slug>', views.detail, name='detail'),

    # ajax
    path('ajax/filters', views.ajax_filter_blog, name='ajax_filter_blog'),
    path('ajax/like-blog', views.ajax_like_blog, name='ajax_like_blog'),
    path('ajax/send-comment', views.ajax_send_comment, name='ajax_send_comment'),
    path('ajax/delete-comment', views.ajax_delete_comment, name='ajax_delete_comment'),
]