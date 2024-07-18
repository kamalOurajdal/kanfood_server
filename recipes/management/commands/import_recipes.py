# your_app/management/commands/import_recipes.py
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Recipe, Category, Nutrition
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Imports recipes into the database'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'recipes/management/commands/recipes.json')
        with open(file_path, 'r', encoding="utf-8") as file:
            recipes = json.load(file)
        i=0
        for recipe in recipes:
            # Get or create author
            author, _ = User.objects.get_or_create(username=recipe['author'])

            # Get or create category
            category, _ = Category.objects.get_or_create(name=recipe['category'])

            # Create the recipe
            new_recipe = Recipe(
                id=recipe['id'],
                title=recipe['title'],
                image="recipe_images/" + recipe['image'],
                description=recipe['description'],
                ingredients=recipe['ingredients'],
                instructions=recipe['instructions'],
                cooking_time=recipe['cooking_time'],
                servings=recipe['servings'],
                author=author,
                is_featured=recipe['is_featured'],
                created_at=recipe['created_at'],
                updated_at=recipe['updated_at']
            )
            new_recipe.save()

            # Add category
            new_recipe.categories.add(category)

            # Create and add nutrition information
            for nutrition_data in recipe['nutrition']:
                Nutrition.objects.create(
                    recipe=new_recipe,
                    name=nutrition_data['name'],
                    value=nutrition_data['value'],
                    unit=nutrition_data['unit']
                )

            self.stdout.write(self.style.SUCCESS('Successfully imported recipe data'))

        self.stdout.write(self.style.SUCCESS('Successfully imported recipes'))
