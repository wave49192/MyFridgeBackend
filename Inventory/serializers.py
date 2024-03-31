from rest_framework import serializers
from .models import Ingredient, Inventory, User
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']
        
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['ingredients', 'owned_by']
