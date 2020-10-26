from django.urls import path

from .views import home, MedicalBookView, lazy_load_records

app_name = 'records'
urlpatterns = [
    path('', home, name='home'),
    path('medical-book/patient<int:patient_id>/', MedicalBookView.as_view(), name='medical-book'),
    path('post/ajax/add-record/patient<int:patient_id>/', MedicalBookView.as_view(), name='add-record'),
    path('post/ajax/lazy-load-records/<int:patient_id>/', lazy_load_records, name='lazy-load-records'),
]
