from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.models import Patient, Doctor

class Record(models.Model):
    content = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)