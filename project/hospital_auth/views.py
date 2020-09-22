from django.contrib.auth import login, logout, views as auth_views
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm
from .models import User, Doctor, Patient
from .mixins import StaffRequiredMixin, DoctorRequiredMixin
from .decorators import doctor_required

class DoctorSignUpView(StaffRequiredMixin, CreateView):
    """
    Only staff users can add a new Doctors
    """
    model = User
    form_class = DoctorSignUpForm
    template_name = 'hospital_auth/doctor_signup_form.html'
    success_url = reverse_lazy('hospital_records:home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'hospital_auth/patient_signup_form.html'

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

@login_required
def logout_view(request):
    logout(request)

    return redirect('hospital_records:home')

class DoctorPatientListView(DoctorRequiredMixin, ListView):
    login_required = True
    model = Patient
    template_name = 'hospital_auth/doctor_patients.html'

    def get_queryset(self):
        # get patients that served only by the authenticated doctor
        object_list = Patient.objects.filter(doctors__pk=
            self.request.user.doctor.id)

        print(object_list)

        return object_list 