
from functools import wraps
from django.http import JsonResponse
import logging

logger = logging.getLogger('django')

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                logger.debug(f"User ID: {request.user.id}, Username: {request.user.username}, Role: {request.user.role}, Allowed roles: {allowed_roles}")
                if request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    logger.warning(f"Permission denied for user {request.user.username} with role {request.user.role}. Required roles: {allowed_roles}")
                    return JsonResponse({'error': 'Permission denied'}, status=403)
            else:
                logger.warning("Authentication required")
                return JsonResponse({'error': 'Authentication required'}, status=401)
        return _wrapped_view
    return decorator

