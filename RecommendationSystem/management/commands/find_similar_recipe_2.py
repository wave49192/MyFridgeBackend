from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
import torch
import torch.nn.functional as F

class RecommendationSystem:
    @staticmethod
    def find_similar_recipes_by_ingredients(favorite_recipe, recipes):
        favorite_ingredients = favorite_recipe['cleaned_ingredients'].split(', ')
        recipe_ingredients = [recipe['cleaned_ingredients'].split(', ') for recipe in recipes]
        
        favorite_embedding = torch.zeros(len(favorite_ingredients))
        for idx, ingredient in enumerate(favorite_ingredients):
            favorite_embedding[idx] = recipe_ingredients[0].index(ingredient) if ingredient in recipe_ingredients[0] else 0
        
        recipe_embeddings = torch.zeros(len(recipes), len(favorite_embedding))
        for i, recipe in enumerate(recipe_ingredients):
            for idx, ingredient in enumerate(favorite_ingredients):
                recipe_embeddings[i][idx] = recipe.index(ingredient) if ingredient in recipe else 0
        
        similarities = F.cosine_similarity(favorite_embedding.unsqueeze(0), recipe_embeddings)
        
        sorted_indices = torch.argsort(similarities, descending=True)
        
        favorite_recipe_index = recipes.index(favorite_recipe)
        sorted_indices = sorted_indices[sorted_indices != favorite_recipe_index]
        
        top_10_similar_recipes = [(recipes[i]['title'], similarities[i].item()) for i in sorted_indices[:10]]
        return top_10_similar_recipes

    @staticmethod
    def find_similar_recipes_by_cuisine(favorite_recipe, recipes):
        favorite_cuisine = favorite_recipe['cuisine_type']
        recipe_cuisines = [recipe['cuisine_type'] for recipe in recipes]
        
        # Create a set of unique cuisine types
        unique_cuisines = set(recipe_cuisines)
        
        # Mapping from cuisine type to index in the embeddings
        cuisine_to_index = {cuisine: i for i, cuisine in enumerate(unique_cuisines)}
        
        favorite_embedding = torch.zeros(1, len(unique_cuisines))
        favorite_index = cuisine_to_index.get(favorite_cuisine)
        if favorite_index is not None:
            favorite_embedding[0][favorite_index] = 1
        
        recipe_embeddings = torch.zeros(len(recipes), len(unique_cuisines))
        for i, cuisine in enumerate(recipe_cuisines):
            recipe_embeddings[i][cuisine_to_index[cuisine]] = 1
        
        similarities = F.cosine_similarity(favorite_embedding, recipe_embeddings, dim=1)
        
        sorted_indices = torch.argsort(similarities, descending=True)
        
        favorite_recipe_index = recipes.index(favorite_recipe)
        sorted_indices = sorted_indices[sorted_indices != favorite_recipe_index]
        
        top_10_similar_recipes = [(recipes[i]['title'], similarities[i].item()) for i in sorted_indices[:10]]
        return top_10_similar_recipes


    @staticmethod
    def recommend_similar_recipes(favorite_recipe):
        recipes_queryset = Recipe.objects.all()
        recipes = [
            {
                'recipe_id': recipe.recipe_id,
                'title': recipe.title,
                'image_url': recipe.image_url,
                'publisher': recipe.publisher,
                'source_url': recipe.source_url,
                'cooking_time': recipe.cooking_time,
                'ingredients': recipe.ingredients,
                'cuisine_type': recipe.cuisine_type,
                'cleaned_ingredients': recipe.cleaned_ingredients
            }
            for recipe in recipes_queryset
        ]
        
        similar_recipes_by_ingredients = RecommendationSystem.find_similar_recipes_by_ingredients(favorite_recipe, recipes)
        print("Similar recipes by ingredients:")
        for recipe, similarity in similar_recipes_by_ingredients:
            print(f"{recipe}: {similarity}")
        
        similar_recipes_by_cuisine = RecommendationSystem.find_similar_recipes_by_cuisine(favorite_recipe, recipes)
        print("\nSimilar recipes by cuisine:")
        for recipe, similarity in similar_recipes_by_cuisine:
            print(f"{recipe}: {similarity}")

class Command(BaseCommand):
    help = 'Recommend similar recipes based on a favorite recipe'

    def handle(self, *args, **kwargs):
        favorite_recipe = {
            "recipe_id": "5ed6604591c37cdc054bc9ec",
            "title": "1-minute berry ice cream",
            "image_url": "http://forkify-api.herokuapp.com/images/2_1_1350376582_lrg6103.jpg",
            "publisher": "Jamie Oliver",
            "source_url": "http://www.jamieoliver.com/recipes/fruit-recipes/1-minute-berry-ice-cream",
            "cooking_time": 45,
            "ingredients": "500 g mixed frozen berries, 150 g fresh blueberries, 7 tbsps runny honey, 500 g natural yoghurt, None  A few sprigs fresh mint, 4  small ice cream cornets optional",
            "cuisine_type": "Mexican",
            "cleaned_ingredients": "mixed frozen berries, fresh blueberries, runny honey, natural yoghurt, None  A few sprigs fresh mint, small ice cream cornets optional"
        }

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(favorite_recipe)
