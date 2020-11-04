from django.urls import path
import django.contrib.auth.views as auth_views 

from .views import (
    PatientSignUpView,
    DoctorSignUpView,
    LoginView,
    logout,
    profile,
    SearchPatient,
    add_doctor_patient,
    SearchDoctor,
)

app_name = 'users'
urlpatterns = [
    path('register/patient/', PatientSignUpView.as_view(), name='register-patient'),
    path('register/doctor/', DoctorSignUpView.as_view(), name='register-doctor'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),

    # the search of the patients by a particular doctor
    path('doctor/<int:doctor_id>/search_patient/', SearchPatient.as_view(), name='search_patient'),
    path('doctor/<int:doctor_id>/add/patient/', add_doctor_patient, name='add_patient'),

    # the search of the doctors by any user to make an appointment
    path('search_doctor/', SearchDoctor.as_view(), name='search_doctor'),
]