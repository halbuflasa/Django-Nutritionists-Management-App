from django import template
from menu.models import Meal

register = template.Library()

@register.filter
def get_meal(meals, meal_type):
    """
    Retrieve a meal of the specified type from a queryset of meals.
    """
    try:
        return meals.get(meal_type=meal_type)
    except Meal.DoesNotExist:
        return None
