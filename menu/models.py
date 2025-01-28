import logging  # For debugging purposes
from datetime import timedelta, date
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from dishes.models import Dish

# Initialize logger
logger = logging.getLogger(__name__)

class Menu(models.Model):
    MENU_TYPES = [
        ('main', 'Main'),
        ('kids', 'Kids'),
        ('vegetarian', 'Vegetarian'),
    ]
    name = models.CharField(max_length=100, blank=True)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if start_date has changed
        original_start_date = None
        if self.pk:  # Only check if the object already exists
            original_start_date = Menu.objects.filter(pk=self.pk).values_list('start_date', flat=True).first()

        # Auto-generate a name if not provided
        if not self.name:
            self.name = f"{self.get_menu_type_display()} Menu"
        
        # Ensure start_date is provided
        if not self.start_date:
            raise ValidationError("A start date is required for the menu.")

        super().save(*args, **kwargs)

        # Recalculate associated days if start_date has changed
        if original_start_date and original_start_date != self.start_date:
            self.update_associated_days()

    def update_associated_days(self):
        """
        Recalculate all associated days' dates based on the new start_date.
        """
        logger.info(f"Updating days for menu: {self.name} with new start_date: {self.start_date}")
        week_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Align the new start_date to the first Saturday
        weekday_offset = (5 - self.start_date.weekday()) % 7
        aligned_start_date = self.start_date + timedelta(days=weekday_offset)

        # Update the dates for all related weeks and days
        for week in self.weeks.all():
            for i, day in enumerate(week.days.all()):
                new_date = aligned_start_date + timedelta(days=(i + (week.week_number - 1) * 7))
                day.date = new_date
                day.save()
                logger.info(f"Updated Day: {day.day_name} to new date: {new_date} for Week {week.week_number}")

    def get_suggested_start_date(self):
        """
        Suggest the next Saturday as the default start date.
        """
        today = date.today()
        # Saturday is weekday 5
        days_until_saturday = (5 - today.weekday()) % 7
        return today + timedelta(days=days_until_saturday)

    def __str__(self):
        return f"{self.name} ({self.get_menu_type_display()})"


class Week(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="weeks")
    week_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Week {self.week_number} - {self.menu.name}"


class Day(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    day_name = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate day name if date is provided
        if self.date:
            self.day_name = self.date.strftime("%A")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.day_name} ({self.date}) - {self.week.menu.name} (Week {self.week.week_number})"


class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="meals")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="meals")

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.day.day_name} (Week {self.day.week.week_number})"


@receiver(post_save, sender=Menu)
def create_weeks_and_days(sender, instance, created, **kwargs):
    """
    Signal to create weeks and days when a new menu is created.
    """
    if created:
        logger.info(f"Creating weeks for menu: {instance.name} with start_date: {instance.start_date}")

        # Fixed day names
        week_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Align the start_date to the first Saturday
        weekday_offset = (5 - instance.start_date.weekday()) % 7
        aligned_start_date = instance.start_date + timedelta(days=weekday_offset)

        for week_num in range(1, 5):  # Create 4 weeks
            week = Week.objects.create(menu=instance, week_number=week_num)
            for i, day_name in enumerate(week_days):
                # Calculate the date for each day in the week
                date = aligned_start_date + timedelta(days=(i + (week_num - 1) * 7))
                Day.objects.create(week=week, day_name=day_name, date=date)
                logger.info(f"Created Day: {day_name} on {date} for Week {week_num}")
