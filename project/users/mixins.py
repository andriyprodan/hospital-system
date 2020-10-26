from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from .decorators import doctor_required

class StaffRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return staff_member_required(view, login_url=settings.LOGIN_URL)

class DoctorRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return doctor_required(view, login_url=settings.LOGIN_URL)