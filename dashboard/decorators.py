from django.http import Http404

def is_employer(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'employer' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap


def is_candidate(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'candidate' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap


def is_blogger(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'blogger' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    
    return wrap