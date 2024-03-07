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
