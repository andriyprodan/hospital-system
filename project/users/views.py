from django.contrib.auth import login, logout, views as auth_views
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.template import loader

from .forms import (
    DoctorSignUpForm,
    PatientSignUpForm,
    LoginForm,
    UserUpdateForm,
    UserProfileUpdateForm,
    DoctorProfileUpdateForm,
    UserSearchForm,
)
from .models import User, Doctor, Patient
from .decorators import particular_doctor_required
from .mixins import StaffRequiredMixin, UserSearchMixin, ParticularDoctorRequiredMixin

class DoctorSignUpView(StaffRequiredMixin, CreateView):
    """
    Only staff users can add a new Doctors
    """
    model = User
    form_class = DoctorSignUpForm
    template_name = 'users/doctor_signup_form.html'
    success_url = reverse_lazy('records:home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'users/patient_signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('records:home')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login_form.html'

@login_required
def logout_view(request):
    logout(request)

    return redirect('records:home')

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.patient
        )
        if request.user.is_doctor:
            d_form = DoctorProfileUpdateForm(request.POST, instance=request.user.doctor)

        cond0 = u_form.is_valid() and p_form.is_valid()
        if request.user.is_doctor:
            if cond0 and d_form.is_valid():
                u_form.save()
                p_form.save()
                d_form.save()
                return redirect('users:profile')
        elif cond0:
            u_form.save()
            p_form.save()
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.patient)
        if request.user.is_doctor:
            d_form = DoctorProfileUpdateForm(instance=request.user.doctor)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'd_form': d_form
    }
    return render(request, 'users/profile.html', context)

class SearchPatient(UserSearchMixin, LoginRequiredMixin, ParticularDoctorRequiredMixin, ListView):
    model = Patient
    template_name = 'users/search_patient.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        
        search_query = self.request.GET.get('q', None)
        if search_query is not None:
            qs = qs.filter(
                Q(user__phone__contains=search_query) |
                Q(user__email__contains=search_query)
            )
        else: # when the doctor first hits the page (without searching)
            # get only doctor's patients
            qs = qs.filter(doctors__pk=self.kwargs['doctor_id'])

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = UserSearchForm()
        context['user_type'] = 'Patient'
        context['table_caption'] = 'Click on the table row to view the patient\'s medical book'
        return context

@particular_doctor_required
def add_doctor_patient(request, doctor_id):
    """
    The view that accepts ajax request with patient id and
    adds patient with that id to the doctor's patient list
    """
    # add a patient to the doctor's patients list
    if request.is_ajax():
        patient = Patient.objects.get(pk=request.POST['patient_id'])   
        request.user.doctor.patients.add(patient)

        # refresh table row with this patient
        new_table_row = loader.render_to_string(
            'users/patient_table_row.html',
            {
                'object': patient,
                'user': request.user
            }
        )
        # package output data and return it as a JSON object
        output_data = {
            'new_table_row': new_table_row,
        }
        return JsonResponse(output_data)
    else:
        return JsonResponse({"error": "Bad request"}, status=400)
    
    # some error occured
    return JsonResponse({"error": ""}, status=400)

class SearchDoctor(UserSearchMixin, LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'users/search_user.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        
        search_query = self.request.GET.get('q', None)
        if search_query is not None:
            qs = qs.filter(
                Q(bio__contains=search_query) |
                Q(spec__contains=search_query)
            )

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = UserSearchForm()
        context['user_type'] = 'Doctor'
        context['table_caption'] = 'Click on the table row to make an appointment with the doctor'
        
        return context