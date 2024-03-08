from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Recipe, RecipeDetails


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
        
class RecipeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeDetails
        fields = ['recipe_id', 'title','image_url', 'publisher','source_url','cooking_time','ingredients']