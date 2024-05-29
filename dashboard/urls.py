from django.urls import path

from .views import main, employer, candidate, blogger

app_name = 'dashboard'

urlpatterns = [
    path('', main.index, name='index'),

    # Employer URL's
    path('employer/complete-register', employer.complete_register, name='employer-complete-register'),
    path('vacnacy/post', employer.post_vacancy, name='post-vacancy'),
    path('vacancy/all', employer.all_vacancy, name='all-vacancy'),

    # Candidate URL's
    path('candidate/complete-register', candidate.complete_register, name='candidate-complete-register'),

    # Blog URL's
    path('blog/post', blogger.post_blog, name='post-blog'),
    path('blog/all', blogger.all_blog, name='all-blog'),
    path('blog/edit/<int:id>', blogger.edit_blog, name='edit-blog'),

    path('blog/editor/upload-image', blogger.upload_editor_image, name='upload-editor-image'),
    path('blog/editor/delete-image', blogger.delete_editor_image, name='delete-editor-image')
]