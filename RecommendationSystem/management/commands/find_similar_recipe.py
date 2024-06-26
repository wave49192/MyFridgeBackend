from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationSystem:
    
    """
    The similarity score are high in the recipe that has a lot of ingredient and low in little ingredient, will fix later.
    The time complexity is high and can not be improved as it needs to do a nested loop in order to compare every word in the list 
    So I will find another way to improve the time complexity by using another algorithm.
    
    -----------UPDATE-------------
    TF-IDF Vectorization then cosine similarity. works fine on many favourite recipe.
    -----------UPDATE-------------
    
    Algorithm tried:
    1 Nltk distance (The Levenshtein distance between two strings: more distance = less alike).
    2 TF-IDF Vectorization then cosine similarity. (will use this one)
    """
    @staticmethod
    def recommend_similar_recipes(input_recipes):
        recipes_queryset = Recipe.objects.all()
        recipes = [
            {
                'recipe_id': recipe.recipe_id,
                'title': recipe.title,
                'image_url': recipe.image_url,
                'cuisine_type': recipe.cuisine_type,
                'cooking_time':recipe.cooking_time,
                'cleaned_ingredients': recipe.cleaned_ingredients
            }
            for recipe in recipes_queryset
        ]
        
        
        # Extracting input ingredients and ingredients for each recipe
        
        input_ingredients = [ingredient.strip() for input_recipe in input_recipes for ingredient in input_recipe['cleaned_ingredients'].split(',')]
        recipe_ingredients = [recipe['cleaned_ingredients'] for recipe in recipes]
        
        # Create TF-IDF vectors
        corpus = recipe_ingredients + [', '.join(input_ingredients)]
        print("all ingredients",corpus)
        
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
        
        feature_names = tfidf_vectorizer.get_feature_names_out()
        
        #all feature in the data
        print("feature name",feature_names)
        
        tfidf_matrix_input = tfidf_matrix[-1]
        tfidf_matrix_recipes = tfidf_matrix[:-1]

        # Calculate cosine similarity between user's input ingredients and recipes
        # it will return the list of similarities score of the input compare to all recipes.[recipe1,recipe2,etc...]
        similarity_scores = cosine_similarity(tfidf_matrix_input,tfidf_matrix_recipes)
        
        
        # Associate similarity scores with recipes
        recipe_similarity_scores = {recipes[i]['recipe_id']: similarity_scores[0][i] for i in range(len(recipes))}
        print("similarity score",recipe_similarity_scores)
        
        # Exclude input recipes from recommendations by setting their scores to 0 (but if there is no recipe_id this will not run)
        for input_recipe in input_recipes:
            recipe_id = input_recipe.get('recipe_id')
            if recipe_id:  # Check if 'recipe_id' exists
                if recipe_id in recipe_similarity_scores:
                    recipe_similarity_scores[recipe_id] = 0
                    
        
        # Sort recipes based on similarity score
        sorted_recipes = sorted(recipes, key=lambda x: recipe_similarity_scores[x['recipe_id']], reverse=True)

        recommended_recipes = [{
            'recipe_id': recipe['recipe_id'],
            'title': recipe['title'],
            'image_url':recipe['image_url'],
            'cuisine_type': recipe['cuisine_type'],
            'cooking_time': recipe['cooking_time'],
        } for recipe in sorted_recipes[:48]]
        # print(recommended_recipes)
        return recommended_recipes



### py manage.py find_similar_recipe
### run this for testing the recommendation function locally only
class Command(BaseCommand):
    help = 'Recommend similar recipes based on a input recipe'

    def handle(self, *args, **kwargs):
        input_recipe = [
    {
        "recipe_id": "5ed6604591c37cdc054bca02",
        "title": "Crusty cheddar pies",
        "cleaned_ingredients": "bread mix"
    }
            ,      {
        "recipe_id": "5ed6604591c37cdc054bcaa7",
        "title": "Cucumber and Feta Rolls",
        "cleaned_ingredients": "potatoes"
    },
        ]

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(input_recipe)
