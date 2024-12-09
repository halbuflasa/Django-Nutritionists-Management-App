from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Nutritionist', 'Nutritionist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Nutritionist')
