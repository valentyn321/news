from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauth_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_groups(disallowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in disallowed_roles:

                return render(request, 'posts/error_creation.html', {})
                
            else:
                return view_func(request, *args, **kwargs)


        return wrapper

    return decorator


