from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
import torch.nn.functional as F
import nltk

nltk.download('punkt')

class RecommendationSystem:

    """
    The similarity score are high in the recipe that has a lot of ingredient and low in little ingredient, will fix later.
    The time complexity is high and can not be improved as it needs to do a nested loop in order to compare every word in the list 
    So I will find another way to improve the time complexity by using another algorithm.
    
    Algorithm tried:
    1 Nltk distance (The Levenshtein distance between two strings: more distance = less alike)
    """
    @staticmethod

    def find_similar_recipes_by_ingredients(favorite_recipe, recipes):
        # Function to calculate the union of ingredients in all favorite recipes
        ingredient_union = lambda favorite_recipes: set().union(*[set(recipe['cleaned_ingredients'].split(', ')) for recipe in favorite_recipes])
        
        # Extracting favorite ingredients and ingredients for each recipe
        favorite_ingredients = ingredient_union(favorite_recipe)
        recipe_ingredients = [recipe['cleaned_ingredients'].split(', ') for recipe in recipes]

        # Dictionary to store similarity scores for each recipe
        similar_recipes_score = {}

        # Calculating similarity score for each recipe
        for recipe, ingredients in zip(recipes, recipe_ingredients):
            similarity_score = 0
            for favorite_ingredient in favorite_ingredients:
                # Calculate minimum edit distance between each favorite ingredient and each ingredient in the recipe
                min_distance = min(nltk.edit_distance(favorite_ingredient, ingredient) for ingredient in ingredients)
                # Normalize the edit distance by dividing by the length of the longer list
                normalized_distance = min_distance / max(len(favorite_ingredient), len(ingredients))
                similarity_score += normalized_distance

            # Store the average similarity score for the recipe
            similar_recipes_score[recipe['recipe_id']] = similarity_score / len(favorite_ingredients)

        return similar_recipes_score

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

        similar_recipes_score = {}
        print("Similar recipes by ingredients:")
        for recipe_id, similarity_score in similar_recipes_by_ingredients.items():
            similar_recipes_score[recipe_id] = similarity_score# sort the similar recipes by score
        recipes_dict = {recipe['recipe_id']: recipe for recipe in recipes}

        similar_recipes = [{'recipe_id': recipe_id, 'title': recipes_dict[recipe_id]['title'], 'similarity_score': score}
                        for recipe_id, score in similar_recipes_score.items()]


        sorted_similar_recipes = sorted(similar_recipes, key=lambda x: x['similarity_score'], reverse=False)
        print("Top 10 similar recipes:")
        for i in range(min(10, len(sorted_similar_recipes))):
            print(f"{i+1}. {sorted_similar_recipes[i]['title']} (similarity score: {sorted_similar_recipes[i]['similarity_score']})")
        return similar_recipes if similar_recipes_score else None


class Command(BaseCommand):
    help = 'Recommend similar recipes based on a favorite recipe'

    def handle(self, *args, **kwargs):
        favorite_recipe = [    
         {
        "recipe_id": "5ed6604591c37cdc054bcfbd",
        "title": "sweet potato (and marshmallow) biscuits",
        "image_url": "http://forkify-api.herokuapp.com/images/6380938927_72dfcfb439a301.jpg",
        "publisher": "Smitten Kitchen",
        "source_url": "http://smittenkitchen.com/blog/2011/11/sweet-potato-and-marshmallow-biscuits/",
        "cooking_time": 75,
        "ingredients": "1 pound sweet potatoes, 0.33 cup buttermilk, 2 cups all-purpose flour, 1 tbsp baking powder, 3 tbsps granulated sugar, 1 tsp ground cinnamon, 0.25 tsp ground nutmeg, 0.25 tsp ground ginger, 0.13 tsp ground cloves, 0.5 tsp table salt, 5 tbsps unsalted butter cold, 1 cup miniature marshmallows",
        "cuisine_type": "Hawaiian",
        "cleaned_ingredients": "pound sweet potatoes, buttermilk, all-purpose flour, baking powder, granulated sugar, ground cinnamon, ground nutmeg, ground ginger, ground cloves, table salt, unsalted butter cold, miniature marshmallows"
    },
    
    ]

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(favorite_recipe)