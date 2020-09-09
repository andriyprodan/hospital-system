from django.shortcuts import render

def home(request):
    return render(request, 'hospital_records/home.html')