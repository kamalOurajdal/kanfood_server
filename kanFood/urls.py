"""
URL configuration for kanFood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


from recipes.views import RecipeListCreate, CategoryListCreate, NutritionListCreate, SavedRecipeListCreate, \
    RecipeDetail, get_nutrition_of_recipe, get_recipes_by_category, search_recipes

urlpatterns = [
    path("", lambda request: HttpResponse("Welcome to KanFood")),
    path('recipes/', RecipeListCreate.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('recipes/<int:recipe_id>/nutrition/', get_nutrition_of_recipe, name='get-nutrition-of-recipe'),
    path('recipes', search_recipes, name='get-nutrition-of-recipe'),



    path('categories/<int:category_id>/recipes/', get_recipes_by_category, name='get-recipes-by-category'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('nutrition/', NutritionListCreate.as_view(), name='nutrition-list-create'),
    path('saved_recipes/', SavedRecipeListCreate.as_view(), name='savedrecipe-list-create'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)