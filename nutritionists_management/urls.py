from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('users/login/'), name='root_redirect'),
    path('secure-admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('patients/', include('patients.urls')),
    path('dishes/', include('dishes.urls')),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)