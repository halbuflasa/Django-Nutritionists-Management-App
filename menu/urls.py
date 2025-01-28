from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('form/', views.menu_form, name='menu_create'),  # For creating a menu
    path('form/<int:menu_id>/', views.menu_form, name='menu_edit'),  # For editing a menu
    path('<int:menu_id>/delete/', views.delete_menu, name='menu_delete'),  # For deleting a menu
    path('', views.menu_list, name='menu_list'),
    path('<int:menu_id>/assign-dishes/', views.assign_dishes, name='assign_dishes'),
]
