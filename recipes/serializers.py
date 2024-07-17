# recipes/serializers.py
from rest_framework import serializers


from .models import Nutrition, Recipe, Category, SavedRecipe

from rest_framework import serializers


# Base message serializer


class NutritionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    value = serializers.DecimalField(max_digits=8, decimal_places=2)
    unit = serializers.CharField(max_length=50)
    class Meta:
        model = Nutrition
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    ingredients = serializers.ListField(child=serializers.CharField())
    instructions = serializers.ListField(child=serializers.CharField())
    cooking_time = serializers.IntegerField()
    servings = serializers.IntegerField()
    image = serializers.ImageField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_featured = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = '__all__'


class SavedRecipeSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    user = serializers.CharField()
    recipe = serializers.CharField()

    class Meta:
        model = SavedRecipe
        fields = '__all__'
