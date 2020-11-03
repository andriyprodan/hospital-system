from django.urls import path
import django.contrib.auth.views as auth_views 

from .views import (
    PatientSignUpView,
    DoctorSignUpView,
    LoginView,
    logout,
    DoctorPatientListView,
    profile
)

app_name = 'users'
urlpatterns = [
    path('register/patient/', PatientSignUpView.as_view(), name='register-patient'),
    path('register/doctor/', DoctorSignUpView.as_view(), name='register-doctor'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    # patiens of a particular doctor
    path('doctor/<int:doctor_id>/patients/', DoctorPatientListView.as_view(), name='doctor_patients'),
    path('doctor<int:doctor_id>/get/ajax/search/patients/', DoctorPatientListView.as_view(), name='search_patients'),
    path('post/ajax/add/patient/', DoctorPatientListView.as_view(), name='add_patient'),
    
]