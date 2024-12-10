from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patients_list, name='patient_profiles_list'),
    path('create/', views.patient_create, name='patient_profile_create'),
]
