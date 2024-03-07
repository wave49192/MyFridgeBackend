from django.shortcuts import render

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from RecommendationSystem.models import Recipe,RecipeDetails

from RecommendationSystem.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
@api_view(['GET'])
def getFoodData(request):
    foodList = {'name': 'Fried chicken', 'cookingTime': 30}
    return Response(foodList)

def getRecipeList(request):
    recipes = Recipe.objects.all()
    data = [{'id':recipe.recipe_id,'title': recipe.title, 'publisher': recipe.publisher, 'image_url': recipe.image_url} for recipe in recipes]
    return JsonResponse(data, safe=False)


def getRecipeDetailList(request):
    recipe_details = RecipeDetails.objects.all()
    data = [{'id':recipeDetail.recipe_id,'title': recipeDetail.title, 'publisher': recipeDetail.publisher, 'image_url': recipeDetail.image_url, 'source_url': recipeDetail.source_url, 'cooking_time': recipeDetail.cooking_time, 'ingredients': recipeDetail.ingredients} for recipeDetail in recipe_details]
    return JsonResponse(data, safe=False)
