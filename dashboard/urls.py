from django.urls import path

from .views import main, employer, candidate, blogger

app_name = 'dashboard'

urlpatterns = [
    path('', main.index, name='index'),
    path('bookmarks', main.bookmarks, name='bookmarks'),
    path('ajax/delete-bookmark', main.ajax_delete_bookmark, name='ajax-delete-bookmark'),

    # Employer URL's
    path('employer/complete-register', employer.complete_register, name='employer-complete-register'),
    path('vacnacy/post', employer.post_vacancy, name='post-vacancy'),
    path('vacancy/all', employer.all_vacancy, name='all-vacancy'),
    path('vacancy/edit/<int:id>', employer.edit_vacancy, name='edit-vacancy'),
    path('employer/edit-account', employer.edit_account, name='employer-edit-account'),
    path('ajax/vacancies', employer.ajax_all_vacancy, name='ajax-all-vacancy'),
    path('ajax/delete-vacancy', employer.ajax_delete_vacancy, name='ajax-delete-vacancy'),

    # Candidate URL's
    path('candidate/complete-register', candidate.complete_register, name='candidate-complete-register'),
    path('your-applies', candidate.your_applies, name='your-applies'),
    path('candidate/edit-account', candidate.edit_account, name='candidate-edit-account'),

    # Blog URL's
    path('blog/post', blogger.post_blog, name='post-blog'),
    path('blog/all', blogger.all_blog, name='all-blog'),
    path('blog/edit/<int:id>', blogger.edit_blog, name='edit-blog'),
    path('ajax/delete-blog', blogger.ajax_delete_blog, name='ajax-delete-blog'),

    path('blog/editor/upload-image', blogger.upload_editor_image, name='upload-editor-image'),
    path('blog/editor/delete-image', blogger.delete_editor_image, name='delete-editor-image')
]