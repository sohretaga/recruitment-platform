from django.urls import path

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path('password-reset', PasswordResetView.as_view(template_name='user/reset-password.html'), name='reset-password'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]