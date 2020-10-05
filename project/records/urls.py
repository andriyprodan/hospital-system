from django.urls import path

from .views import home, MedicalBookView

app_name = 'records'
urlpatterns = [
    path('', home, name='home'),
    path('medical-book/patient<int:patient_id>/', MedicalBookView.as_view(), name='medical-book'),
    path('post/ajax/add-record/patient<int:patient_id>/', MedicalBookView.as_view(), name='add-record'),
]
