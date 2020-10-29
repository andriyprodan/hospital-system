from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers
# stuff for lazy loading
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from users.models import Patient
from .models import Record
from .forms import AddRecordForm

def home(request):
    return render(request, 'records/home.html')

# used in MedicalBookView and lazy_load_records
def check_user(request, patient_id):
    if not request.user.is_active:
        raise Http404()
    # user viewing his own medical book
    if request.user.id == patient_id:
        return
    if request.user.is_doctor:
        # check if the patient is on the doctor's patient list
        if not request.user.doctor.patients.filter(pk=patient_id).exists():
            raise Http404()

class MedicalBookView(LoginRequiredMixin, ListView):
    """
    Medical book of a particular patient (all records about patient)
    """
    model = Record
    template_name = 'records/medical_book.html'
    ordering = '-created_at'

    def get(self, request, *args, **kwargs):

        check_user(request, kwargs['patient_id'])

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # adding a new record to the patient's medical book
        if request.is_ajax():
            form = AddRecordForm(request.POST)
            # save the data and fetch the object in an instance
            if form.is_valid():
                instance = form.save(request.user.doctor.id, kwargs['patient_id'])
                # send to client side.
                new_record_html = loader.render_to_string(
                    'records/records_list.html',
                    {'object_list': [instance,]}
                )
                # package output data and return it as a JSON object
                output_data = {
                    'new_record_html': new_record_html,
                }
                return JsonResponse(output_data)

            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def get_queryset(self):
        self.queryset = Record.objects.filter(patient__pk=self.kwargs['patient_id'])
        qs = super().get_queryset()
        # get only first ten records, the other records will be loaded using lazy_load_records view
        return qs[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_form'] = AddRecordForm()
        return context

def lazy_load_records(request, patient_id):
    """
    lazy load the records when the user scroll down to the last record
    """

    if not request.is_ajax():
        raise Http404()

    check_user(request, patient_id)

    page = request.POST.get('page')
    # get all records of the patient with id from the url keyword argument
    records = Record.objects.filter(patient__pk=patient_id).order_by('-created_at')
    results_per_page = 10
    paginator = Paginator(records, results_per_page)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(2)
    except EmptyPage:
        records = None
    # build a html records list with the paginated records
    records_html = loader.render_to_string(
        'records/records_list.html',
        {'object_list': records}
    )
    # package output data and return it as a JSON object
    output_data = {
        'records_html': records_html,
        'has_next': records.has_next() if records else False
    }
    return JsonResponse(output_data)
