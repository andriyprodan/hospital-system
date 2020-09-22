from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    if instance.is_patient:
        instance.patient.save()