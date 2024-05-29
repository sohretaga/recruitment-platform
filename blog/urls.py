from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:slug>', views.detail, name='detail'),

    # ajax
    path('ajax/filters', views.ajax_filter_blog, name='ajax_filter_blog'),
]