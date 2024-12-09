from django.db import models
from django.conf import settings

class HealthData(models.Model):
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
    bmr = models.FloatField(null=True, blank=True)
    daily_calories = models.FloatField(null=True, blank=True)

    def calculate_bmr_and_calories(self):
        if self.gender == 'male':
            bmr = 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        else:
            bmr = 655.09 + (9.563 * self.weight) + (1.849 * self.height) - (4.675 * self.age)

        activity_multiplier = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'heavy': 1.725,
            'very heavy': 1.9,
        }[self.activity_level]

        self.bmr = bmr
        self.daily_calories = bmr * activity_multiplier

    def save(self, *args, **kwargs):
        self.calculate_bmr_and_calories()
        super().save(*args, **kwargs)
