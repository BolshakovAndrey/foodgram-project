import json

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from api.models import FavoriteRecipe, User, Follow
from recipes.models import Recipe, Ingredient, Purchase


class FavoriteView(View):

    def post(self, request):
        recipe_id = json.load(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite, created = FavoriteRecipe.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if created:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class SubscribeView(View):

    def post(self, request):
        author_id = json.load(request.body).get('id')
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
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class GetIngredientsView(View):

    def get(self, request):
        queryset = request.GET.get('query')
        ingredients = list(Ingredient.objects.filter(
            name_istartwith=queryset.annotate(
                title=F('name'),
                dimension=F('dimension')
            )).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class PurchasesView(View):

    def post(self, request):
        recipe_id = json.load(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        purchaselist, created = Purchase.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if created:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        """ Удаляем подписку если она существует. """
        count, _ = Purchase.objects.filter(
            user=request.user,
            recipe=recipe_id
        ).delete()
        return JsonResponse({'success': True if count else False})
