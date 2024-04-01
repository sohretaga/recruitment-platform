from django.urls import path

from .views import main, employer, candidate

app_name = 'dashboard'

urlpatterns = [
    path('employer/complete-register', employer.complete_register, name='employer-complete-register'),
    path('post-vacancy', employer.post_vacancy, name='post-vacancy'),
]