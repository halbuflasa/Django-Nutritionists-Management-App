from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirect the root URL to the login page
    path('', lambda request: redirect('users/login/'), name='root_redirect'),
    
    # Secure admin access
    path('secure-admin/', admin.site.urls),
    
    # Include users app URLs for login, logout, and dashboard
    path('users/', include('users.urls')),
    
    # Include patients app URLs for managing health data
    path('patients/', include('patients.urls')),
]
