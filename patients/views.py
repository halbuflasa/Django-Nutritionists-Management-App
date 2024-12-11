from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import calendar

from .models import PatientProfile, PatientMenuItem
from .forms import PatientForm, PatientMenuItemForm
from dishes.models import Dish  # Import the Dish model
from datetime import datetime

@login_required
def patients_list(request):
    patients = PatientProfile.objects.filter(user=request.user)
    return render(request, 'patients/patient_profiles_list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk, user=request.user)

    # Get year and month from GET parameters or use current month
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Handle month overflow
    if month > 12:
        month = 1
        year += 1
    elif month < 1:
        month = 12
        year -= 1

    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    month_days = list(cal.itermonthdates(year, month))

    # Break month_days into weeks (6 weeks * 7 days)
    weeks = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

    # Get this month's menu items
    start_of_month = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_of_month = date(year, month, last_day)
    menu_items = patient.menu_items.filter(date__range=(start_of_month, end_of_month))

    # Build a dictionary of date -> list of (dish, menu_item_id)
    menu_dict = {}
    for item in menu_items:
        menu_dict.setdefault(item.date, []).append((item.dish, item.id))

    # Fetch all dishes to display in the modal for adding a dish
    all_dishes = Dish.objects.all()

    # Get the full name of the month
    month_name = datetime(year, month, 1).strftime('%B')

    return render(request, 'patients/patient_profile_detail.html', {
        'patient': patient,
        'year': year,
        'month': month,
        'month_name': month_name,  # Pass the month's name to the template
        'weeks': weeks,
        'menu_dict': menu_dict,
        'dishes': all_dishes,
    })

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


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients:patient_profiles_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


@login_required
def add_menu_item(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id, user=request.user)
    if request.method == 'POST':
        form = PatientMenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.patient = patient
            menu_item.save()
            return redirect('patients:patient_detail', pk=patient_id)
    else:
        initial_date = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
        form = PatientMenuItemForm(initial={'date': initial_date})
    return render(request, 'patients/add_menu_item.html', {'form': form, 'patient': patient})


@login_required
def remove_menu_item(request, patient_id, menu_item_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id, user=request.user)
    menu_item = get_object_or_404(PatientMenuItem, pk=menu_item_id, patient=patient)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('patients:patient_detail', pk=patient_id)
    return render(request, 'patients/remove_menu_item.html', {'menu_item': menu_item, 'patient': patient})
