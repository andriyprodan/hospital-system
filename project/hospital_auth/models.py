from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class User(AbstractUser):
    phone = models.CharField(max_length=32)

    is_doctor = models.BooleanField('doctor status', default=False)
    is_patient = models.BooleanField('patient status', default=False)

class Specialization(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("Specialization name"))

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spec = models.ManyToManyField(Specialization)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor)
