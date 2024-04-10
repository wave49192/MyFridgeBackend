from rest_framework import serializers

from RecommendationSystem.serializers import RecipeSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'favourite_recipes']

class UserFavoriteRecipesSerializer(serializers.ModelSerializer):
    favourite_recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['favourite_recipes']