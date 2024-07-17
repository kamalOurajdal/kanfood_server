from datetime import datetime

from django.utils.decorators import method_decorator
from loguru import logger
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.serializers import RecipeSerializer, CategorySerializer, NutritionSerializer, SavedRecipeSerializer
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from recipes.models import Recipe, Category, Nutrition, SavedRecipe

from django.views import View


# Create your views here.

class RecipePagination(PageNumberPagination):
    page_size = 10  # default page size
    max_page_size = 100

class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination


class RecipeDetail(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NutritionListCreate(generics.ListCreateAPIView):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer


class SavedRecipeListCreate(generics.ListCreateAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer


@api_view(['GET'])
def get_nutrition_of_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        nutrition = Nutrition.objects.filter(recipe=recipe)
        serializer = NutritionSerializer(nutrition, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_recipes_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        recipes = Recipe.objects.filter(categories=category)
        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_recipes(request):
    query = request.GET.get('q', '')
    print(query)
    if query:

        recipes = Recipe.objects.filter(title__icontains=query)
        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)