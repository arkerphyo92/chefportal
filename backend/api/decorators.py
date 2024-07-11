# utils/decorators.py

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.auth  # Authenticated user from JWT
            # Check if the user is a superuser
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if the group exists
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                return HttpResponse("Not Found: Group not found.", status=404)

            # Check if the user belongs to the group
            if not user.groups.filter(name=group_name).exists():
                return HttpResponseForbidden("Unauthorized: You don't have permission to access this page.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def group_required_no_auth(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user  # Authenticated user from session or basic auth
            # Check if the user is authenticated
            if not user.is_authenticated:
                return HttpResponseForbidden("Unauthorized: You need to log in to access this page.")

            # Check if the user is a superuser
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if the group exists
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                return HttpResponse("Not Found: Group not found.", status=404)

            # Check if the user belongs to the group
            if not user.groups.filter(name=group_name).exists():
                return HttpResponseForbidden("Unauthorized: You don't have permission to access this page.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
