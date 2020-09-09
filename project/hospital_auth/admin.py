from django.contrib import admin

from .models import Specialization, User, Doctor, Patient

admin.site.register(Specialization)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)