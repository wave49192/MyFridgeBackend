# management/commands/load_data.py

import csv
from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe, RecipeDetails

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.load_data()

    def load_data(self):
        # Load data from recipe.csv
        with open('recipe.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipe = Recipe.objects.create(
                    recipe_id=row['recipe_id'],
                    title=row['title'],
                    publisher=row['publisher'],
                    image_url=row['image_url']
                )
        # Load data from recipe_details.csv
        with open('recipe_details.csv', 'r') as detailsfile:
            details_reader = csv.DictReader(detailsfile)
            for detail_row in details_reader:
                if detail_row['recipe_id'] == row['recipe_id']:
                    RecipeDetails.objects.create(
                        recipe=recipe,
                        source_url=detail_row['source_url'],
                        cooking_time=detail_row['cooking_time'],
                        ingredients=detail_row['ingredients']
                    )
