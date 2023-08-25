# Generated by Django 4.2.2 on 2023-08-23 08:04

import datetime
from django.db import migrations, models
from django.utils.text import slugify
from meals.models import Meal

def generate_slugs(apps, schema_editor):
    for meal in Meal.objects.all():
        meal.slug = slugify(meal.name)
        meal.save()

class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_alter_meal_dateadded_alter_meal_imageurl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        # migrations.RunPython(generate_slugs),
    ]
