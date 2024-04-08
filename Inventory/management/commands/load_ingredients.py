# management/commands/load_ingredients.py

import csv
import json
from django.core.management.base import BaseCommand
from Inventory.models import Ingredient
from RecommendationSystem.models import Recipe

class Command(BaseCommand):
    help = 'Load data from JSON files into the database'

    def handle(self, *args, **kwargs):
        self.load_data()

    def load_data(self):
        with open('ingredients.json') as f:
            data = json.load(f)

        for group_data in data:
            group_name = group_data['group_name']
            # Iterate over each ingredient in the group
            for ingredient_name in group_data['ingredients']:
                # Create an Ingredient instance and save it to the database
                Ingredient.objects.create(name=ingredient_name, group=group_name)
