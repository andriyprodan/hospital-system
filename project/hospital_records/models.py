from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class MedicalBook(models.Model):
    """
    Medical Book of the particular Patient
    that stores all the records about Patient illnesses
    """
    patient = models.OneToOneField(UserModel, on_delete=models.CASCADE)

class Record(models.Model):
    content = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    medical_book = models.ForeignKey(MedicalBook, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE)