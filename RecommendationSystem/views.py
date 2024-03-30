from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


from RecommendationSystem.models import Recipe

from RecommendationSystem.serializers import GroupSerializer, UserSerializer,RecipeSerializer,IngredientSerializer


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
def getRecipe(request):
    recipes = Recipe.objects.all()

    serializer = RecipeSerializer(recipes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getIngredients(request):
    recipes = Recipe.objects.all()

    serializer = IngredientSerializer(recipes,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchRecipe(request):
    # Get the recipe name from the query parameters
    recipe_name = request.GET.get('name', '')

    # If a recipe name is provided, filter the recipes by name
    if recipe_name:
        recipes = Recipe.objects.filter(title__icontains=recipe_name)
    else:
        # If no recipe name is provided, return an error response or default data
        return Response({'error': 'Please provide a recipe name'}, status=400)

    # Serialize the filtered recipes using the serializer
    serializer = RecipeSerializer(recipes, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getRecipeDetails(request):
    # Get the recipe ID from the query parameters
    recipe_id = request.GET.get('recipe_id', '')

    # Check if recipe_id is provided
    if not recipe_id:
        return Response({'error': 'Please provide a recipe id'}, status=400)

    # Retrieve the specific recipe object by its ID
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)

    # Serialize the recipe using the serializer
    serializer = RecipeSerializer(recipe)
    
    return Response(serializer.data)