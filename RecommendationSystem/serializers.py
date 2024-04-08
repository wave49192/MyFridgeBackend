from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Recipe
        
        
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['recipe_id', 'title','image_url', 'publisher','source_url','cooking_time','ingredients','cuisine_type','cleaned_ingredients']
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [ 'recipe_id','title','cuisine_type','cleaned_ingredients']