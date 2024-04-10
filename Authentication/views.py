from urllib.parse import urlencode
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response

from Inventory.models import Inventory
from RecommendationSystem.models import Recipe
from RecommendationSystem.serializers import RecipeSerializer
from .mixins import PublicApiMixin, ApiErrorsMixin
from .utils import google_get_access_token, google_get_user_info
from Authentication.models import User
from Authentication.serializers import UserFavoriteRecipesSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        
        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'
    
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}'
        access_token = google_get_access_token(code=code, 
                                               redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                'picture': str(user_data.get('picture', ''))
            }
            return Response(response_data)
        except User.DoesNotExist:
            username = user_data['email'].split('@')[0]
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = User.objects.create(
                username=username,
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                registration_method='google'
            )
            
            inventory = Inventory.objects.create(
                owned_by=user
            )
                     
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                'picture': str(user_data.get('picture', ''))
            }
            return Response(response_data)
        
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post', 'get', 'delete'], url_path='favourites')
    def favourites(self, request, pk):
        if request.method == 'POST':
            try:
                user = self.get_object()
                recipe = Recipe.objects.filter(recipe_id=request.data.get('recipe')['recipe_id']).first()
            
                user.favourite_recipes.add(recipe)
                
                return JsonResponse({'message': 'Recipe added to favorites successfully.'}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        if request.method == 'GET':
            try:                
                user = self.get_object()
                serialized_recipe = UserFavoriteRecipesSerializer(user)
                
                return Response(serialized_recipe.data)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        if request.method == 'DELETE':
            try:
                user = self.get_object()
                recipe = recipe = Recipe.objects.filter(recipe_id=request.data.get('recipe')['recipe_id']).first()

                user.favourite_recipes.remove(recipe)
                
                return JsonResponse({'message': 'Recipe removed to favorites successfully.'}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=500)