from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish
from .forms import DishForm
from django.contrib.auth.decorators import login_required


@login_required
# List all dishes
def dishes_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes/dishes_list.html', {'dishes': dishes})


@login_required
# View details of a single dish
def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'dishes/dish_detail.html', {'dish': dish})


@login_required
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dishes:dishes_list')  # Use the app namespace
    else:
        form = DishForm()
    return render(request, 'dishes/add_dish.html', {'form': form})

@login_required
def update_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('dishes:dishes_list')  # Use the namespaced URL
    else:
        form = DishForm(instance=dish)
    return render(request, 'dishes/add_dish.html', {'form': form})


@login_required
# Delete a dish
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        dish.delete()
        return redirect('dishes:dishes_list')
    return render(request, 'dishes/delete_dish.html', {'dish': dish})
