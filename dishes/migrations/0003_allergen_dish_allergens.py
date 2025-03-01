# Generated by Django 5.1.4 on 2025-01-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0002_remove_dish_allergens_remove_dish_calories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('icon', models.ImageField(upload_to='allergen_icons/')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='allergens',
            field=models.ManyToManyField(blank=True, related_name='dishes', to='dishes.allergen'),
        ),
    ]
