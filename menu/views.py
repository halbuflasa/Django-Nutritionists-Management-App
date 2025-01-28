from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Menu, Week, Day, Meal
from dishes.models import Dish, Allergen, NutritionInfo
from .forms import MenuForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Prefetch

@login_required
def menu_form(request, menu_id=None):
    """Handle both menu creation and editing."""
    if menu_id:
        menu = get_object_or_404(Menu, id=menu_id)
    else:
        menu = None

    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')  # Redirect to the menu list view
    else:
        form = MenuForm(instance=menu)
        # Set default suggested start date if creating a new menu
        if not menu and not form.initial.get('start_date'):
            form.initial['start_date'] = Menu().get_suggested_start_date()

    return render(request, 'menu/menu_form.html', {'form': form, 'menu': menu})


@login_required
def delete_menu(request, menu_id):
    """View for deleting a menu."""
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        raise Http404("The menu you're trying to delete does not exist.")

    if request.method == "POST":
        menu.delete()
        return redirect('menu:menu_list')  # Redirect to menu list after deletion

    return render(request, 'menu/delete_menu.html', {'menu': menu})
@login_required
def menu_list(request):
    """View to display all menus with their details."""
    menus = Menu.objects.prefetch_related('weeks__days')
    return render(request, 'menu/menu_list.html', {'menus': menus})



@login_required
def assign_dishes(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    weeks = menu.weeks.prefetch_related(
        Prefetch('days__meals', queryset=Meal.objects.select_related('dish'))
    )
    dishes = Dish.objects.all()
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    nutrition_infos = NutritionInfo.objects.values('id', 'diet_plan', 'menu').distinct()

    # Parse expanded weeks from GET or initialize for POST
    expanded_weeks = request.GET.get('expanded_weeks', '').split(',')
    expanded_weeks = [int(w) for w in expanded_weeks if w.isdigit()]

    if request.method == "POST":
        day_id = request.POST.get('day_id')
        meal_type = request.POST.get('meal_type')
        dish_id = request.POST.get('dish_id')
        delete_meal = request.POST.get('delete_meal')

        if delete_meal:  # Handle meal deletion
            Meal.objects.filter(day_id=day_id, meal_type=meal_type).delete()

        elif day_id and meal_type and dish_id:  # Handle adding or updating a dish
            day = get_object_or_404(Day, id=day_id)
            dish = get_object_or_404(Dish, id=dish_id)
            Meal.objects.update_or_create(
                day=day,
                meal_type=meal_type,
                defaults={'dish': dish}
            )

        # Determine the expanded week based on the affected day
        week = Week.objects.filter(days__id=day_id).first()
        if week and week.id not in expanded_weeks:
            expanded_weeks.append(week.id)

        # Redirect with updated expanded weeks to persist the state
        return redirect(f"{request.path}?expanded_weeks={','.join(map(str, expanded_weeks))}")

    # Filters for GET request
    search_query = request.GET.get('search', '').strip()
    nutrition_filter = request.GET.get('nutrition_info', '')

    if search_query:
        dishes = dishes.filter(name__icontains=search_query)
    if nutrition_filter:
        dishes = dishes.filter(nutrition_infos__id=nutrition_filter).distinct()

    # AJAX request handling for filtering dishes
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('menu/_dish_cards.html', {'dishes': dishes})
        return JsonResponse({'html': html})

    return render(request, 'menu/assign_dishes.html', {
        'menu': menu,
        'weeks': weeks,
        'dishes': dishes,
        'meal_types': meal_types,
        'nutrition_infos': nutrition_infos,
        'search_query': search_query,
        'nutrition_filter': nutrition_filter,
        'expanded_weeks': expanded_weeks,  # Ensure expanded weeks are passed to the template
    })


