from django.shortcuts import redirect

def logout_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:main-index')
        else:
            return function(request, *args, **kwargs)

    return wrap