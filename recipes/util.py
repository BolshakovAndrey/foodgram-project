from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, IngredientQuantity, Tag


def create_ingredients_amounts(instance, form_data):
    names = [
        value for name, value in form_data.items()
        if name.startswith('nameIngredient_')
    ]
    units = [
        value for name, value in form_data.items()
        if name.startswith('valueIngredient_')
    ]
    ingredients_amounts = [
        IngredientQuantity(
            ingredient=get_object_or_404(Ingredient, name=ingredient),
            units=int(unit),
            recipe=instance
        )
        for ingredient, unit in zip(names, units)
    ]
    IngredientQuantity.objects.bulk_create(ingredients_amounts)


def get_all_tags():
    return Tag.objects.all()


def get_filters(request, queryset):
    filters = request.GET.getlist('filters')
    if filters:
        qs = queryset.filter(tag__slug__in=filters).distinct()
        return qs
    return queryset
