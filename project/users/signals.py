from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Patient

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Patient profiles are created automatically for every user
    """
    if created:
        Patient.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    instance.patient.save()