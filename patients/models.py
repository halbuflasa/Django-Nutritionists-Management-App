from django.db import models
from django.conf import settings
from dishes.models import Dish

class PatientProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('heavy', 'Heavy'),
        ('very heavy', 'Very Heavy'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    weight = models.FloatField()
    height = models.FloatField()
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    bmr = models.FloatField(null=True, blank=True)
    daily_calories = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_bmr_and_calories(self):
        if self.gender == 'male':
            self.bmr = 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        else:
            self.bmr = 655.09 + (9.563 * self.weight) + (1.849 * self.height) - (4.675 * self.age)
        
        activity_multiplier = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'heavy': 1.725,
            'very heavy': 1.9,
        }
        self.daily_calories = self.bmr * activity_multiplier[self.activity_level]
        self.save()

    def __str__(self):
        return self.name

class PatientMenuItem(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='menu_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='patient_assignments')
    date = models.DateField('Menu date')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.dish.name} on {self.date}"
