from django.contrib import admin

# Register your models here.

from .models import Nutrition, Recipe, Category, SavedRecipe


class NutritionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'unit')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cooking_time', 'servings', 'author', 'is_featured')
    search_fields = ('title', 'author__username')
    list_filter = ('is_featured', 'categories')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'saved_at')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('user', 'recipe')


admin.site.register(Nutrition, NutritionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SavedRecipe, SavedRecipeAdmin)
