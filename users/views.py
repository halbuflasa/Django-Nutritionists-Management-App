from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.role == 'Admin':
        # Redirect Admin to the admin panel
        return redirect('/secure-admin/')
    elif request.user.role == 'Nutritionist':
        # Render the Nutritionist dashboard
        return render(request, 'users/dashboard.html')
    else:
        # Handle unexpected roles (optional)
        return redirect('/users/login/')
