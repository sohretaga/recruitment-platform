from typing import Any
from django.shortcuts import redirect
from django.urls import reverse

class RegistrationCompletionMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        if not request.user.is_superuser and request.user.is_authenticated:

            if not request.user.is_registration_complete:
                employer_complete_register_path = reverse('dashboard:employer-complete-register')
                candidate_complete_register_path = reverse('dashboard:candidate-complete-register')

                if request.user.user_type == 'employer' and request.path != employer_complete_register_path:
                    return redirect(employer_complete_register_path)

                elif request.user.user_type == 'candidate' and request.path != candidate_complete_register_path:
                    return redirect(candidate_complete_register_path)

        return self.get_response(request)