from django.db import models

from ..hospital_auth.models import Doctor, Patient

class Appointment(models.Model):
    """
    Appointments can be created by patients and doctors.
    When a patient creates an Appointment with a particular doctor,
    the doctor is sent a request to confirm it
    """
    # the time when the meeting is to take place
    time = models.DateTimeField()
    # complaint in illness
    complaint = models.TextField(max_length=256)
    # fields that indicate whether a doctor confirms the appointment
    is_confirmed = models.BooleanField(default=False)

    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

