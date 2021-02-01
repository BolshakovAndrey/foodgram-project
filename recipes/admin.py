from django.contrib import admin

from api.models import Favorite
from .models import Tag, Recipe, Ingredient, Amount, Purchase


class IngredientQuantityInline(admin.TabularInline):
    """Description of the Inline "IngredientQuantity" model fields for the administration site"""
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Description of the "Recipe" model fields for the administration site"""
    filter_horizontal = ('tag', 'ingredients',)
    list_filter = ('author', 'name', 'tag',)
    list_display = (
        'name', 'author', 'count_favorited'
    )
    ordering = ['name', ]
    autocomplete_fields = ('ingredients',)
    readonly_fields = ('count_favorited',)

    def count_favorited(self, obj):
        count = Favorite.objects.filter(recipe=obj).count()
        return count


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Description of the "Tag" model fields for the administration site"""
    list_display = ('id', 'name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Description of the "Ingredient" model fields for the administration site"""
    list_display = ('id', 'name', 'unit',)
    search_fields = ('^name',)


@admin.register(Amount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Description of the "Ingredient Quantity" model fields for the administration site"""
    list_display = ('id', 'ingredient', 'recipe', 'units',)
    search_fields = ('ingredient',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Description of the "Purchase" model fields for the administration site"""
    list_display = ('id', 'user',)
