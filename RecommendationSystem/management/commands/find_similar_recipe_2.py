from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
import torch
import torch.nn.functional as F

class RecommendationSystem:
    @staticmethod
    def find_similar_recipes_by_ingredients(favorite_recipe, recipes):
        ingredient_union = lambda favorite_recipes: set().union(*[set(recipe['cleaned_ingredients'].split(', ')) for recipe in favorite_recipes])
        favorite_ingredients = ingredient_union(favorite_recipe) #list of all ingredient that are in the favourite recipe
        recipe_ingredients = [recipe['cleaned_ingredients'].split(', ') for recipe in recipes] #a specific recipe that i want to compare with.
        
        #
       #todo fill in the code by finding similarity
     

        
        top_10_similar_recipes = []
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
        
        similar_recipes_score = {}
        print("Similar recipes by ingredients:")
        ## fill in this code to store all the similarity score of every recipe comparing to the favourite recipe.
        


class Command(BaseCommand):
    help = 'Recommend similar recipes based on a favorite recipe'

    def handle(self, *args, **kwargs):
        favorite_recipe =     [{
        "recipe_id": "5ed6604591c37cdc054bcac4",
        "title": "Pizza Dip",
        "image_url": "http://forkify-api.herokuapp.com/images/Pizza2BDip2B12B500c4c0a26c.jpg",
        "publisher": "Closet Cooking",
        "source_url": "http://www.closetcooking.com/2011/03/pizza-dip.html",
        "cooking_time": 60,
        "ingredients": "4 oz cream cheese room temperature, 0.25 cup sour cream, 0.25 cup mayonnaise, 0.5 cup mozzarella grated, 0.25 cup parmigiano reggiano grated, 1 cup pizza sauce, 0.5 cup mozzarella shredded/grated, 0.25 cup parmigiano reggiano grated, 2 oz pepperoni sliced, 2 tbsps green pepper sliced, 2 tbsps black olives sliced",
        "cuisine_type": "German",
        "cleaned_ingredients": "cream cheese room temperature, sour cream, mayonnaise, mozzarella grated, parmigiano reggiano grated, pizza sauce, mozzarella shredded/grated, parmigiano reggiano grated, pepperoni sliced, green pepper sliced, black olives sliced"
    },    {
        "recipe_id": "5ed6604591c37cdc054bcd08",
        "title": "Pomegranate Yogurt Bowl",
        "image_url": "http://forkify-api.herokuapp.com/images/breakfast_yogurt_bowlc10d.jpg",
        "publisher": "101 Cookbooks",
        "source_url": "http://www.101cookbooks.com/archives/pomegranate-yogurt-bowl-recipe.html",
        "cooking_time": 60,
        "ingredients": "None  For each bowl:, None  A big dollop of greek yogurt, 2 tbsps fresh pomegranate juice, None  A drizzle of honey, None  A handful of puffed quinoa crisps, None  Sprinkling of toasted sunflower seeds, None  Optional: whole pomegranate seeds or fresh/dried rose petals a bit of bee pollen",
        "cuisine_type": "Italian",
        "cleaned_ingredients": "None  For each bowl:, None  A big dollop of greek yogurt, fresh pomegranate juice, None  A drizzle of honey, None  A handful of puffed quinoa crisps, None  Sprinkling of toasted sunflower seeds, None  Optional: whole pomegranate seeds or fresh/dried rose petals a bit of bee pollen"
    },
                               ]

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(favorite_recipe)