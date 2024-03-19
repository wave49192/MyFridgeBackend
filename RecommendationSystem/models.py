# models.py
from django.db import models



class Recipe(models.Model):
    recipe_id = models.CharField(max_length=100,primary_key=True)
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    publisher = models.CharField(max_length=255)
    source_url = models.URLField()
    cooking_time = models.IntegerField()
    ingredients = models.TextField()
    cuisine_type = models.CharField(max_length=255)
    cleaned_ingredients = models.TextField()

    def __str__(self):
        return self.title

