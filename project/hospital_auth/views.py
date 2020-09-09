from django.contrib.auth import login, views as auth_views
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm
from .models import User

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'hospital_auth/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hospital_records:home')

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'hospital_auth/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hospital_records:home')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'hospital_auth/login_form.html'