# management/commands/load_data.py

import csv
from django.core.management.base import BaseCommand
from RecommendationSystem.models import Recipe

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.load_data()

    def load_data(self):
        # Load data from recipe_details.csv
        with open('recipe_details.csv', 'r', encoding='utf-8') as recipesfile:
            recipe_reader = csv.DictReader(recipesfile)
            for recipe_row in recipe_reader:
                Recipe.objects.create(
                    recipe_id=recipe_row['recipe_id'],
                    title=recipe_row['title'],
                    image_url=recipe_row['image_url'],
                    publisher=recipe_row['publisher'],
                    source_url=recipe_row['source_url'],
                    cooking_time=int(recipe_row['cooking_time']),
                    ingredients=recipe_row['ingredients']
                )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
