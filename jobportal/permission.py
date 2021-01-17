from django.core.exceptions import PermissionDenied


def user_is_recruiter(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == 'recruiter':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_candidate(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == 'candidate':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_admin(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
