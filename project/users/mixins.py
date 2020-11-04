from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.db.models import Q
from django.http import Http404

from .decorators import particular_doctor_required

class StaffRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return staff_member_required(view, login_url=settings.LOGIN_URL)

class UserSearchMixin(object):
    """
    Used in the PatientSearch and DoctorSearch
    """
    def get_queryset(self):
        qs = super().get_queryset()

        search_query = self.request.GET.get('q', None)
        if search_query or search_query == '':
            qs = qs.filter(
                Q(user__first_name__contains=search_query) |
                Q(user__last_name__contains=search_query) |
                Q(user__phone__contains=search_query) |
                Q(user__email__contains=search_query)
            )
        return qs

class ParticularDoctorRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return particular_doctor_required(view)
