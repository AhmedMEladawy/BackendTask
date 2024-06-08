
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from functools import wraps



class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'manager']

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.role not in allowed_roles:
                raise PermissionDenied("You don't have permission to perform this action.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

