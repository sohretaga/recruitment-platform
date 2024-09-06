from django.urls import path

from .views import main, employer, candidate, blogger, controller

app_name = 'dashboard'

urlpatterns = [
    path('', main.index, name='index'),
    path('bookmarks', main.bookmarks, name='bookmarks'),
    path('ajax/delete-bookmark', main.ajax_delete_bookmark, name='ajax-delete-bookmark'),

    path('faqs', main.faqs, name='faqs'),
    path('faqs/add', main.add_faq, name='add-faq'),
    path('faqs/edit/<int:id>', main.edit_faq, name='edit-faq'),
    path('ajax/delete-faq', main.ajax_delete_faq, name='ajax-delete-faq'),

    # Employer URL's
    path('employer/complete-register', employer.manage_account, name='employer-complete-register'),
    path('employer/vacnacy/post', employer.post_vacancy, name='post-vacancy'),
    path('employer/vacancy/all', employer.all_vacancy, name='all-vacancy'),
    path('employer/vacancy/edit/<int:id>', employer.edit_vacancy, name='edit-vacancy'),
    path('ajax/vacancies', employer.ajax_all_vacancy, name='ajax-all-vacancy'),
    path('ajax/delete-vacancy', employer.ajax_delete_vacancy, name='ajax-delete-vacancy'),
    path('ajax/fetch-definition', employer.ajax_fetch_definition, name='ajax-fetch-definition'),
    path('ajax/auto-fetch-definition', employer.ajax_auto_fetch_definition, name='auto-ajax-fetch-definition'),

    # Candidate URL's
    path('candidate/complete-register', candidate.manage_account, name='candidate-complete-register'),
    path('applications', candidate.your_applies, name='applications'),
    path('ajax/delete-apply', candidate.ajax_delete_apply, name='ajax-delete-apply'),

    # Blog URL's
    path('blog/post', blogger.post_blog, name='post-blog'),
    path('blog/all', blogger.all_blog, name='all-blog'),
    path('blog/comments', blogger.comments, name='comments'),
    path('blog/edit/<int:id>', blogger.edit_blog, name='edit-blog'),
    path('ajax/delete-blog', blogger.ajax_delete_blog, name='ajax-delete-blog'),
    path('ajax/delete-comment', blogger.ajax_delete_comment, name='ajax-delete-comment'),
    path('ajax/manage-comment-status', blogger.ajax_manage_comment_status, name='ajax-manage-comment-status'),
    path('ajax/edit-comment', blogger.ajax_edit_comment, name='ajax-edit-comment'),
    path('blog/editor/upload-image', blogger.upload_editor_image, name='upload-editor-image'),

    # Controller URL's
    path('controller/vacancy/all', controller.all_vacancies, name='controller-all-vacancies'),
    path('controller/ajax/vacancies', controller.ajax_all_vacancies, name='ajax-controller-all-vacancies'),
    path('controller/ajax/manage-approval-level', controller.ajax_manage_approval_level, name='ajax-controller-manage-approval-level'),
    path('controller/ajax/update-published-date', controller.ajax_update_published_date, name='ajax-controller-update-published-date'),
]