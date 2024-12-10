from django.shortcuts import render, redirect  # Make sure 'redirect' is imported
from django.contrib.auth.decorators import login_required

# Fake data for Patient Profiles
FAKE_PATIENTS = [
    {
        'name': 'John Doe',
        'age': 35,
        'gender': 'male',
        'weight': 75.5,
        'height': 175.0,
        'activity_level': 'moderate',
        'contact_number': '123-456-7890',
        'bmr': 1700.0,
        'daily_calories': 2500.0,
    },
    {
        'name': 'Jane Smith',
        'age': 28,
        'gender': 'female',
        'weight': 60.0,
        'height': 160.0,
        'activity_level': 'light',
        'contact_number': '987-654-3210',
        'bmr': 1400.0,
        'daily_calories': 2000.0,
    },
]

# List patients
@login_required
def patients_list(request):
    return render(request, 'patients/patient_profiles_list.html', {'patients': FAKE_PATIENTS})

# Create patient form
@login_required
def patient_create(request):
    if request.method == 'POST':
        # Simulate saving data for now
        return redirect('patients:patient_profiles_list')
    return render(request, 'patients/patient_profile_create.html')
