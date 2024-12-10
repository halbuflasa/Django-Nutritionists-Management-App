from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'allergens', 'recipe', 'ingredients', 'image', 'diet_plan', 'calories', 'protein', 'carbs', 'fat', 'portion_size']
        widgets = {
            'allergens': forms.CheckboxSelectMultiple()
        }
