from django.urls import path

from .views import home

app_name = 'hospital_records'
urlpatterns = [
    path('', home, name='home')
]
