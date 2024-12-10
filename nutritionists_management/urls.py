from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static  # Import for serving media files

urlpatterns = [
    # Redirect the root URL to the login page
    path('', lambda request: redirect('users/login/'), name='root_redirect'),
    
    # Secure admin access
    path('secure-admin/', admin.site.urls),
    
    # Include users app URLs for login, logout, and dashboard
    path('users/', include('users.urls')),
    
    # Include patients app URLs for managing health data
    path('patients/', include('patients.urls')),

    # Include dishes app URLs for managing dishes
    path('dishes/', include('dishes.urls')),

  
]

# Add this line to serve media files during development
if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
