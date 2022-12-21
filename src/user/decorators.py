from django.shortcuts import redirect


def unauthorised_user(view_func):
    #restrict page for authorised user
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task-list')
        return view_func(request, *args, **kwargs)
    return wrapper_func
