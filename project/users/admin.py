from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Specialization, User, Doctor, Patient

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields = ('id',)
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor', 'is_patient',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_doctor', 'is_patient')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Patient)