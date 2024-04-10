# Generated by Django 5.0.3 on 2024-04-09 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
        ('RecommendationSystem', '0002_recipe_cleaned_ingredients_recipe_cuisine_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_recipes',
            field=models.ManyToManyField(blank=True, default=[], to='RecommendationSystem.recipe'),
        ),
    ]
