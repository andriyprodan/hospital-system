from django.urls import path
import django.contrib.auth.views as auth_views 

from .views import (
    PatientSignUpView,
    DoctorSignUpView,
    LoginView,
    logout,
)

app_name = 'hospital_auth'
urlpatterns = [
    path('register/patient/', PatientSignUpView.as_view(), name='register-patient'),
    path('register/doctor/', DoctorSignUpView.as_view(), name='register-doctor'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='hospital_auth/logout.html'), name='logout'),
]