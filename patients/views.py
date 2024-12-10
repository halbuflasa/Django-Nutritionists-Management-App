from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile
from .forms import PatientForm

# List all patients
@login_required
def patients_list(request):
    patients = PatientProfile.objects.filter(user=request.user)  # Filter by logged-in user
    return render(request, 'patients/patient_profiles_list.html', {'patients': patients})

# View a specific patient's details
@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk, user=request.user)
    return render(request, 'patients/patient_profile_detail.html', {'patient': patient})

# Create a new patient
@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.calculate_bmr_and_calories()
            patient.save()
            return redirect('patients:patient_profiles_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_profile_create.html', {'form': form})

# Update an existing patient
@login_required
def patient_update(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.calculate_bmr_and_calories()
            patient.save()
            return redirect('patients:patient_profiles_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_profile_create.html', {'form': form})
# Delete a patient
@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients:patient_profiles_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})