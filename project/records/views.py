from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core import serializers

from users.models import Patient
from .models import Record
from .forms import AddRecordForm

def home(request):
    return render(request, 'records/home.html')

class MedicalBookView(ListView):
    """
    Medical book(all records about patient) of a particular patient
    """
    model = Record
    template_name = 'records/medical_book.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_doctor:
            # check whether the doctor has a patient in his/her patients list
            if not request.user.doctor.patients.filter(pk=kwargs['patient_id']).exists():
                raise Http404('You don\'t have access to this page')
        elif request.user.is_patient:
            if request.user.patient.id != kwargs['patient_id']:
                raise Http404('You don\'t have access to this page')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = AddRecordForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save(request.user.doctor.id, kwargs['patient_id'])
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def get_queryset(self):
        self.queryset = Record.objects.filter(patient__pk=self.kwargs['patient_id'])
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_form'] = AddRecordForm()
        return context