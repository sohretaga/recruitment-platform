from django.urls import path

from .views import employer, candidate

app_name = 'dashboard'

urlpatterns = [
    path('employer/complete-register', employer.complete_register, name='employer-complete-register'),
]