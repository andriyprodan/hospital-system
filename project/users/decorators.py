from django.core.exceptions import PermissionDenied

def particular_doctor_required(func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            if not request.user.is_doctor:
                raise PermissionDenied
            elif request.user.doctor.id != kwargs['doctor_id']:
                raise PermissionDenied
            
        return func(request, *args, **kwargs)
    return _wrapped_view