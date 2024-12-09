from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'role')}),  # Role is included here
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')},
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Automatically set is_staff and is_superuser based on role
    def save_model(self, request, obj, form, change):
        if obj.role == 'Admin':
            obj.is_staff = True
            obj.is_superuser = True
        else:
            obj.is_staff = False
            obj.is_superuser = False
        if not change:  # If creating a new user
            obj.is_active = True  # Ensure the user is active by default
        super().save_model(request, obj, form, change)

    # Generalized permission check
    def has_permission(self, request):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'Admin')

    def has_module_permission(self, request):
        return self.has_permission(request)

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request)

admin.site.register(User, CustomUserAdmin)
