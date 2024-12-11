from django import forms
from .models import PatientProfile, PatientMenuItem
from dishes.models import Dish

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'name', 'age', 'gender', 'weight', 'height', 
            'activity_level', 'contact_number'
        ]

class PatientMenuItemForm(forms.ModelForm):
    class Meta:
        model = PatientMenuItem
        fields = ['dish', 'date']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'type': 'date'
                }
            ),
        }
