from django import forms
from .models import PatientProfile

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'name', 'age', 'gender', 'weight', 'height', 
            'activity_level', 'contact_number'
        ]