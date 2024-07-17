import os

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.JSONField()
    instructions = models.JSONField()
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    servings = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Nutrition(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='nutrition')
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.recipe.title}"

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"