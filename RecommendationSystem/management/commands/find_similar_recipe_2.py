from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
import torch.nn.functional as F
import nltk

nltk.download('punkt')

class RecommendationSystem:
    @staticmethod
    def find_similar_recipes_by_ingredients(favorite_recipe, recipes):
        ingredient_union = lambda favorite_recipes: set().union(*[set(recipe['cleaned_ingredients'].split(', ')) for recipe in favorite_recipes])
        favorite_ingredients = ingredient_union(favorite_recipe)
        recipe_ingredients = [recipe['cleaned_ingredients'].split(', ') for recipe in recipes]

        similar_recipes_score = {}

        for recipe, ingredients in zip(recipes, recipe_ingredients):
            similarity_score = 0
            for favorite_ingredient in favorite_ingredients:
                similarity_score += nltk.edit_distance(favorite_ingredient, ingredients)

            similarity_score = similarity_score / len(favorite_ingredients)

            similar_recipes_score[recipe['recipe_id']] = similarity_score

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


        sorted_similar_recipes = sorted(similar_recipes, key=lambda x: x['similarity_score'], reverse=True)
        print("Top 10 similar recipes:")
        for i in range(min(10, len(sorted_similar_recipes))):
            print(f"{i+1}. {sorted_similar_recipes[i]['title']} (similarity score: {sorted_similar_recipes[i]['similarity_score']})")
        return similar_recipes if similar_recipes_score else None


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