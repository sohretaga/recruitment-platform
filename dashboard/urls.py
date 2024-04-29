from django.urls import path

from .views import main, employer, candidate, blogger

app_name = 'dashboard'

urlpatterns = [
    path('', main.index, name='index'),

    path('employer/complete-register', employer.complete_register, name='employer-complete-register'),
    path('post-vacancy', employer.post_vacancy, name='post-vacancy'),

    # Candidate URL's
    path('candidate/complete-register', candidate.complete_register, name='candidate-complete-register'),

    path('blog/post', blogger.post_blog, name='post-blog'),
    path('blog/all', blogger.all_blog, name='all-blog'),
]