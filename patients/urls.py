from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patients_list, name='patient_profiles_list'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('create/', views.patient_create, name='patient_create'),
    path('update/<int:pk>/', views.patient_update, name='patient_update'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),
]
