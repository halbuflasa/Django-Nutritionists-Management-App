from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, NutritionInfo, Allergen
from .forms import DishForm
from .forms import AllergenForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required

# Inline formset for NutritionInfo
NutritionInfoFormSet = inlineformset_factory(
    Dish, NutritionInfo,
    fields=['diet_plan', 'size', 'menu', 'calories', 'protein', 'carbs', 'fat'],
    extra=1,  # Display one empty form by default
    can_delete=True  # Allow deleting rows
)

@login_required
def dishes_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes/dishes_list.html', {'dishes': dishes})

@login_required
def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    nutrition_infos = dish.nutrition_infos.all()  # Retrieve all related NutritionInfo objects
    allergens = dish.allergens.all()  # Retrieve related allergens
    return render(
        request, 
        'dishes/dish_detail.html', 
        {'dish': dish, 'nutrition_infos': nutrition_infos, 'allergens': allergens}
    )


@login_required
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        formset = NutritionInfoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            dish = form.save(commit=False)  # Save the dish instance without committing
            dish.save()  # Save the dish to generate its ID
            form.save_m2m()  # Save the ManyToMany relationships (e.g., allergens)
            formset.instance = dish  # Link the formset to the dish
            formset.save()  # Save NutritionInfo rows
            return redirect('dishes:dishes_list')
        else:
            # Debugging invalid form or formset
            print("Dish Form Errors:", form.errors)
            print("Nutrition Formset Errors:", formset.errors)
    else:
        form = DishForm()
        formset = NutritionInfoFormSet()
    return render(request, 'dishes/add_dish.html', {'form': form, 'formset': formset})


@login_required
def update_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        formset = NutritionInfoFormSet(request.POST, instance=dish)
        if form.is_valid() and formset.is_valid():
            form.save()  # Save the updated dish instance, including allergens
            formset.save()  # Save updated NutritionInfo rows
            return redirect('dishes:dishes_list')
        else:
            # Debugging invalid form or formset
            print("Dish Form Errors:", form.errors)
            print("Nutrition Formset Errors:", formset.errors)
    else:
        form = DishForm(instance=dish)
        formset = NutritionInfoFormSet(instance=dish)
    return render(request, 'dishes/add_dish.html', {'form': form, 'formset': formset})

@login_required
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        dish.delete()
        # Redirect to the dishes list after deletion
        return redirect('dishes:dishes_list')
    return render(request, 'dishes/delete_dish.html', {'dish': dish})

@login_required
def manage_allergens(request):
    allergens = Allergen.objects.all()
    if request.method == 'POST':
        form = AllergenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dishes:manage_allergens')
    else:
        form = AllergenForm()
    return render(request, 'dishes/manage_allergens.html', {'form': form, 'allergens': allergens})
