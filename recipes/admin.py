from django.contrib import admin
from .models import Tag, Recipe, Ingredient, Amount, Purchase


class IngredientQuantityInline(admin.TabularInline):
    """Description of the Inline "IngredientQuantity" model fields for the administration site"""
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Description of the "Recipe" model fields for the administration site"""
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'pub_date', 'author', 'favorite_recipes')
    list_filter = ('author',)
    empty_value_display = '-пусто-'
    search_fields = ('author', 'name', 'tag')
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
