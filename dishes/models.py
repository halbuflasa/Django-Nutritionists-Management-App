from django.db import models

class Dish(models.Model):
    DIET_CHOICES = [
        ('balanced', 'Balanced Diet'),
        ('keto', 'Keto'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('paleo', 'Paleo'),
    ]

    ALLERGEN_CHOICES = [
        ('gluten', 'Gluten'),
        ('fish', 'Fish'),
        ('nuts', 'Nuts'),
        ('dairy', 'Dairy'),
        ('soy', 'Soy'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    allergens = models.ManyToManyField('Allergen', blank=True)
    recipe = models.TextField()
    ingredients = models.TextField()
    image = models.ImageField(upload_to='dish_images/')
    diet_plan = models.CharField(max_length=20, choices=DIET_CHOICES, default='balanced')
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    portion_size = models.FloatField()

    def __str__(self):
        return self.name

class Allergen(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='allergen_icons/')

    def __str__(self):
        return self.name
