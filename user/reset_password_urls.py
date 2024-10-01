from django.urls import path, reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView,
)

urlpatterns = [
    path('password-reset', PasswordResetView.as_view(template_name='user/reset-password.html'), name='reset-password'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='user/password-reset-done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='user/password-reset-confirm.html',
        success_url=reverse_lazy('user:sign-in'),
        ), name='password_reset_confirm'),
]