from django import forms
from .models import Dish, NutritionInfo, Allergen

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            'name', 
            'description', 
            'meal_type',  # Added field for meal or snack selection
            'meal_category',  # Added field for meal category (breakfast, lunch, dinner)
            'recipe', 
            'ingredients', 
            'image',
            'allergens'
        ]
        widgets = {
            'meal_category': forms.Select(attrs={'class': 'form-control'}),  # Optional styling
            'allergens': forms.CheckboxSelectMultiple(),  # Display allergens as checkboxes
        }

    def clean(self):
        cleaned_data = super().clean()
        meal_type = cleaned_data.get('meal_type')
        meal_category = cleaned_data.get('meal_category')

        # Validate meal category only for meals
        if meal_type == 'meal' and not meal_category:
            self.add_error('meal_category', 'Meal category is required for meals.')
        elif meal_type == 'snack' and meal_category:
            self.add_error('meal_category', 'Snacks should not have a meal category.')

        return cleaned_data  # Return the cleaned data directly



# Form for managing NutritionInfo dynamically (used in inline formsets)
class NutritionInfoForm(forms.ModelForm):
    class Meta:
        model = NutritionInfo
        fields = ['id','diet_plan', 'size', 'menu', 'calories', 'protein', 'carbs', 'fat']
        widgets = {
            'diet_plan': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AllergenForm(forms.ModelForm):
    class Meta:
        model = Allergen
        fields = ['name', 'icon']
        widgets = {
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': 'Enter the allergen name (e.g., Gluten, Dairy).',
            'icon': 'Upload an icon to represent this allergen.',
        }
