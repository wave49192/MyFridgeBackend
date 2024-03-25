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
    TF-IDF Vectorization then cosine similarity. works fine on single favourite recipe.
    -----------UPDATE-------------
    
    Algorithm tried:
    1 Nltk distance (The Levenshtein distance between two strings: more distance = less alike).
    2 TF-IDF Vectorization then cosine similarity.
    """
    @staticmethod
    def recommend_similar_recipes(favorite_recipe):
        recipes_queryset = Recipe.objects.all()
        recipes = [
            {
                'recipe_id': recipe.recipe_id,
                'title': recipe.title,
                'cleaned_ingredients': recipe.cleaned_ingredients
            }
            for recipe in recipes_queryset
        ]
        
        # Extracting favorite ingredients and ingredients for each recipe
        favorite_ingredients = [ingredient.strip() for ingredient in favorite_recipe[0]['cleaned_ingredients'].split(',')]
        recipe_ingredients = [recipe['cleaned_ingredients'] for recipe in recipes]
        
        # Create TF-IDF vectors
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(recipe_ingredients + [' '.join(favorite_ingredients)])
        
        # Calculate cosine similarity between user's favorite ingredients and recipes
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # Associate similarity scores with recipes
        recipe_similarity_scores = {recipes[i]['recipe_id']: similarity_scores[0][i] for i in range(len(recipes))}
        
        # Sort recipes based on similarity score
        sorted_recipes = sorted(recipes, key=lambda x: recipe_similarity_scores[x['recipe_id']], reverse=True)

        # Print recommended recipes
        print("Top 10 similar recipes:")
        for i, recipe in enumerate(sorted_recipes[:10], 1):
            print(f"{i}. {recipe['title']} (similarity score: {recipe_similarity_scores[recipe['recipe_id']]:.4f})")

class Command(BaseCommand):
    help = 'Recommend similar recipes based on a favorite recipe'

    def handle(self, *args, **kwargs):
        favorite_recipe = [
            {
                "recipe_id": "5ed6604591c37cdc054bcfbd",
                "title": "sweet potato (and marshmallow) biscuits",
                "cleaned_ingredients": "pound sweet potatoes, buttermilk, all-purpose flour, baking powder, granulated sugar, ground cinnamon, ground nutmeg, ground ginger, ground cloves, table salt, unsalted butter cold, miniature marshmallows"
            }
        ]

        self.stdout.write("Finding similar recipes...\n")
        RecommendationSystem.recommend_similar_recipes(favorite_recipe)
