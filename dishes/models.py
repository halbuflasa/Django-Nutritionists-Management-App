from django.db import models


class Allergen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='allergen_icons/')
    
    def __str__(self):
        return self.name


class Dish(models.Model):
    MEAL_TYPE_CHOICES = [
        ('meal', 'Meal'),
        ('snack', 'Snack'),
    ]

    MEAL_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    recipe = models.TextField()
    ingredients = models.TextField()
    image = models.ImageField(upload_to='dish_images/')
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES, default='meal')
    meal_category = models.CharField(
        max_length=10, choices=MEAL_CATEGORY_CHOICES, blank=True, null=True
    )  # Optional for snacks
    allergens = models.ManyToManyField(Allergen, blank=True, related_name="dishes")  # Added allergens field

    def __str__(self):
        return self.name


class NutritionInfo(models.Model):
    DIET_PLAN_CHOICES = [
        ('low_carb', 'Low Carb'),
        ('balanced', 'Balanced Diet'),
        ('vegetarian', 'Vegetarian'),
        ('muscle_gain', 'Muscle Gain'),
    ]

    SIZE_CHOICES = [
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('xlarge', 'X-Large'),
        ('xxlarge', 'XX-Large'),
    ]

    MENU_CHOICES = [
        ('main', 'Main Menu'),
        ('vegetarian', 'Vegetarian Menu'),
        ('kids', 'Kids Menu'),
    ]

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='nutrition_infos')
    diet_plan = models.CharField(max_length=20, choices=DIET_PLAN_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    menu = models.CharField(max_length=20, choices=MENU_CHOICES)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return f"{self.diet_plan} - {self.size} - {self.menu}"
