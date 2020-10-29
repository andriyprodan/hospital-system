from django import forms

from .models import Record
from users.models import User, Doctor

class AddRecordForm(forms.ModelForm):
    content = forms.CharField(max_length=2048, widget=forms.Textarea)

    class Meta:
        model = Record
        fields = ['content']
    
    def save(self, doctor_id, patient_id):
        """
        Here we rewrite save method to get doctor_id and patient_id from POST AJAX request
        """
        record = super().save(commit=False)
        record.doctor = Doctor.objects.get(pk=doctor_id)
        record.patient = User.objects.get(pk=patient_id)
        record.save()
        return record
