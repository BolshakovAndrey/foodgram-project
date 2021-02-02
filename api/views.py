import json

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from api.models import Favorite, Follow, User
from recipes.models import Ingredient, Purchase, Recipe


class FavoriteView(View):
    """
    view Favorite
    """

    def post(self, request):
        """
        Adding a Recipe to Favorites
        """
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if created:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        """
        Deleting a Recipe from Favorites
        """

        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class SubscribeView(View):
    """
    view Subscribe
    """

    def post(self, request):
        """
        Subscribe the author.
        """
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        if request.user == author:
            return JsonResponse({'success': False})

        follow, created = Follow.objects.get_or_create(
            user=request.user, author=author
        )
        if created:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, author_id):
        """
        Unsubscribe the author.
        """

        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class GetIngredientsView(View):
    """
    creates AJAX request for ingredients
    """

    def get(self, request):
        queryset = request.GET.get('query')
        ingredients = list(Ingredient.objects.filter(
            name__istartswith=queryset).annotate(
            title=F('name'), dimension=F('unit')).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class PurchasesView(View):
    """
    view Purchase
    """

    def post(self, request):
        """
        Adding a recipe to the shopping list
        """

        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        purchaselist, created = Purchase.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if created:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        """
        Removing a prescription from the shopping list.
        """

        count, _ = Purchase.objects.filter(
            user=request.user,
            recipe=recipe_id,
        ).delete()

        return JsonResponse({'success': True if count else False})
