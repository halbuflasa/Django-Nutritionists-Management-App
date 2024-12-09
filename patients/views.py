from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def create_profile(request):
    return HttpResponse("Create Patient Profile")

@login_required
def show_profiles(request):
    return HttpResponse("Show Patient Profiles")
