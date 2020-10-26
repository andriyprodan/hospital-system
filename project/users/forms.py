from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site

from .models import User, Doctor, Patient, Specialization

def send_password_by_email(password, send_to):
    # send email to the user with email and password
    current_site = Site.objects.get_current()
    
    mail_message = f"""
    You have been registered at site {current_site.domain}
    Login: {send_to}
    Password: {password}
    """
    send_mail(
        subject=f'Registration at {current_site.domain}',
        message=mail_message,
        from_email=None,
        recipient_list=[send_to]
    )

class DoctorSignUpForm(forms.ModelForm):
    spec = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name', 'spec')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        password = get_random_string()
        # set random password for the user
        user.set_password(password)
        # send password to the newly created user
        send_password_by_email(password=password, send_to=self.cleaned_data.get('email'))
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.spec.add(*self.cleaned_data.get('spec'))
        return user

class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")

class PatientSearchForm(forms.Form):
    search_str = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'id': 'search-patient'}),
        label='Find patient using first name, last name, email or phone number (without "+" sign)',
        required=False
        )