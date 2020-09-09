from django.urls import path

from .views import PatientSignUpView, DoctorSignUpView, LoginView

app_name = 'hospital_auth'
urlpatterns = [
    path('register/patient/', PatientSignUpView.as_view(), name='register-patient'),
    path('register/doctor/', DoctorSignUpView.as_view(), name='register-doctor'),
    path('login/', LoginView.as_view(), name='login'),
]