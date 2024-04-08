from rest_framework import serializers
from .models import Ingredient, Inventory, InventoryItem, User
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'group']

class InventoryItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    class Meta:
        model = InventoryItem
        fields = ['id', 'ingredient', 'quantity', 'unit']
        
class InventorySerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True, read_only=True)
    class Meta:
        model = Inventory
        fields = ['id', 'items', 'owned_by']
