from django.http import Http404
from django.contrib.auth.decorators import login_required


def is_employer(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'employer' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap

def is_candidate(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'candidate' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap

def is_blogger(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'blogger' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap