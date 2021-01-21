from django.contrib import admin
from .models import Tag, Recipe, Ingredient, IngredientQuantity, Purchase


class IngredientQuantityInline(admin.TabularInline):
    """Description of the Inline "IngredientQuantity" model fields for the administration site"""
    model = Recipe.ingredient.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Description of the "Recipe" model fields for the administration site"""
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'pub_date', 'author', 'favorite_recipes')
    list_filter = ('author',)
    empty_value_display = '-пусто-'
    search_fields = ('author', 'title', 'tag')
    ordering = ('-pub_date',)
    readonly_fields = ('favorite_recipes',)
    inlines = (IngredientQuantityInline,)

    def favorite_recipes(self, instance):
        """The number of additions of recipe to favorites."""
        return instance.favorite_recipe.count()

    favorite_recipes.short_description = 'в избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Description of the "Tag" model fields for the administration site"""
    list_display = ('id', 'title',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Description of the "Ingredient" model fields for the administration site"""
    list_display = ('id', 'title', 'dimension',)
    search_fields = ('^title',)


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    """Description of the "Ingredient Quantity" model fields for the administration site"""
    list_display = ('id', 'ingredient', 'recipe', 'quantity',)
    search_fields = ('ingredient',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Description of the "Purchase" model fields for the administration site"""
    list_display = ('id', 'user',)
