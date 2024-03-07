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
        with open('recipe.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Recipe.objects.create(
                    recipe_id=row['recipe_id'],
                    title=row['title'],
                    publisher=row['publisher'],
                    image_url=row['image_url']
                )

        # Load data from recipe_details.csv
        with open('recipe_details.csv', 'r', encoding='utf-8') as detailsfile:
            details_reader = csv.DictReader(detailsfile)
            for detail_row in details_reader:
                RecipeDetails.objects.create(
                    recipe_id=detail_row['recipe_id'],
                    title=detail_row['title'],
                    image_url=detail_row['image_url'],
                    publisher=detail_row['publisher'],
                    source_url=detail_row['source_url'],
                    cooking_time=int(detail_row['cooking_time']),
                    ingredients=detail_row['ingredients']
                )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
