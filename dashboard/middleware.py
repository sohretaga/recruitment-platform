from typing import Any
from django.shortcuts import redirect
from django.urls import reverse

class RegistrationCompletionMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        if not request.user.is_superuser and request.user.is_authenticated:

            if not request.user.is_registration_complete:
                
                if request.user.user_type == 'employer' and request.path != reverse('dashboard:employer-complete-register'):
                    return redirect(reverse('dashboard:employer-complete-register'))

                elif request.user.user_type == 'candidate' and request.path != reverse('dashboard:candidate-complete-register'):
                    return redirect(reverse('dashboard:candidate-complete-register'))

        return self.get_response(request)