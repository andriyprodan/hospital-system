from django.urls import path

from .views import home

app_name = 'records'
urlpatterns = [
    path('', home, name='home')
]
