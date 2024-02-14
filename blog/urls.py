from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('detail', views.detail, name='detail'),
    path('grid', views.grid, name='grid')
]