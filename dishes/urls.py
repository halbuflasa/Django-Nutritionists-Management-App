from django.urls import path
from . import views

urlpatterns = [
    path('', views.dishes_list, name='dishes_list'),
    path('<int:pk>/', views.dish_detail, name='dish_detail'),
    path('add/', views.add_dish, name='add_dish'),
    path('update/<int:pk>/', views.update_dish, name='update_dish'),
    path('delete/<int:pk>/', views.delete_dish, name='delete_dish'),
]
