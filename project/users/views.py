from django.contrib.auth import login, logout, views as auth_views
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.http import Http404
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import (
    DoctorSignUpForm,
    PatientSignUpForm,
    LoginForm,
    PatientSearchForm,
    UserUpdateForm,
    UserProfileUpdateForm,
    DoctorProfileUpdateForm
)
from .models import User, Doctor, Patient
from .mixins import StaffRequiredMixin

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

class DoctorPatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'users/doctor_patients.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        # doctor searching for patients
        search_query = self.request.GET.get('q', None)
        if search_query or search_query == '':
            qs = qs.filter(
                Q(user__first_name__contains=search_query) |
                Q(user__last_name__contains=search_query) |
                Q(user__phone__contains=search_query) |
                Q(user__email__contains=search_query)
            )
        else:
            qs = qs.filter(doctors__pk=self.kwargs['doctor_id'])

        return qs.order_by('user__first_name').order_by('user__last_name')

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            if not request.user.is_doctor:
                raise Http404('You don\'t have access to this page')
            elif request.user.doctor.id != self.kwargs['doctor_id']:
                raise Http404('You don\'t have access to this page')

        if request.is_ajax(): # search of the patients
            # render only piece of the template(patients list)
            self.template_name = 'users/patients_list.html'

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # add a patient to the doctor's patients list
        if request.is_ajax():
            patient = Patient.objects.get(pk=request.POST['patient_id'])   
            request.user.doctor.patients.add(patient)
            return JsonResponse({"success": True}, status=200)
        
        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PatientSearchForm()

        # used to show "add user" button in the table of patients
        # the button appears only when the doctor starts searching for patients
        if self.request.GET.get('q'):
            context['is_search'] = True

        return context

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