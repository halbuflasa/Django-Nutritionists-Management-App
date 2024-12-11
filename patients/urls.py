from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patients_list, name='patient_profiles_list'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('create/', views.patient_create, name='patient_create'),
    path('update/<int:pk>/', views.patient_update, name='patient_update'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),

    # New URL patterns for menu items
    path('<int:patient_id>/add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('<int:patient_id>/remove_menu_item/<int:menu_item_id>/', views.remove_menu_item, name='remove_menu_item'),
]
