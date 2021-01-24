from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, IngredientQuantity


def save_recipe(ingredients, recipe):
    recipe_ingredients = []

    for title, quantity in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        rec_ingredient = IngredientQuantity(
            quantity=quantity, ingredient=ingredient, recipe=recipe
        )
        recipe_ingredients.append(rec_ingredient)

    IngredientQuantity.objects.bulk_create(recipe_ingredients)


def get_ingredients_from_form(request):
    ingredients = {}

    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = request.POST[
                f'valueIngredient_{_[1]}'
            ]

    return ingredients

