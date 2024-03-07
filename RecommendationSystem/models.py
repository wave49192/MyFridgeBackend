# models.py
from django.db import models

class Recipe(models.Model):
    recipe_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    image_url = models.URLField()

    def __str__(self):
        return self.title

class RecipeDetails(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, primary_key=True)
    source_url = models.URLField()
    cooking_time = models.IntegerField()
    ingredients = models.TextField()

    def __str__(self):
        return self.recipe.title

# script to load CSV data
import csv
from .models import Recipe, RecipeDetails
from django.db import transaction

@transaction.atomic
def load_data_from_csv(file1_path, file2_path):
    # Load data from file1.csv
    with open(file1_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Recipe.objects.create(
                recipe_id=row['recipe_id'],
                title=row['title'],
                publisher=row['publisher'],
                image_url=row['image_url']
            )

    # Load data from file2.csv
    with open(file2_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipe = Recipe.objects.get(recipe_id=row['recipe_id'])
            RecipeDetails.objects.create(
                recipe=recipe,
                source_url=row['source_url'],
                cooking_time=row['cooking_time'],
                ingredients=row['ingredients']
            )

# In your Django views or management commands, call the function like this:
file1_path = './recipe.csv'
file2_path = './recipeDetail.csv'
load_data_from_csv(file1_path, file2_path)
