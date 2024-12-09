from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('profiles/create/', views.create_profile, name='patient_profile_create'),
    path('profiles/show/', views.show_profiles, name='patient_profiles_list'),
]
