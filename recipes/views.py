import csv
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from recipes.models import Favorite, Follow, Ingredient, \
    Purchase, Recipe, User

from .forms import RecipeForm
from .util import create_ingredients_amounts, get_all_tags, get_filters


class RecipeListView(ListView):
    """
    Main page with recipes
    """
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'index.html'
    paginate_by = 6
    template_name_field = 'recipes'

    def get_queryset(self):
        queryset = super().get_queryset()
        return get_filters(self.request, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
        Adds a new recipe.
        After validating the form and creating a new recipe,
        the author is redirected to the index page.
    """
    form_class = RecipeForm
    template_name = 'formCreateChangeRecipe.html'
    success_url = 'index'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        form_data = form.data

        ingredients = [
            key for key in form_data if key.startswith('nameIngredient_')
        ]
        if not ingredients:
            form.add_error(
                'description',
                'Необходимо указать хотя бы один ингредиент для рецепта'
            )
            return self.form_invalid(form)

        ing_name = form_data['nameIngredient_1']
        ingredients_list = Ingredient.objects.values('name')
        if not ingredients_list.filter(name=ing_name).exists():
            form.add_error(
                'description',
                'Необходимо выбирать ингредиент из выпадающего списка'
            )
            return self.form_invalid(form)
        instance.save()
        create_ingredients_amounts(instance, form_data)
        form.save_m2m()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})

        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update recipe
    After validating the form and updating recipe,
    the author is redirected to the recipe page.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'formCreateChangeRecipe.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        form_data = form.data
        instance.amount_recipes.all().delete()
        ingredients = [
            key for key in form_data if key.startswith('nameIngredient_')
        ]
        if not ingredients:
            form.add_error(
                'description',
                'Необходимо указать хотя бы один ингредиент для рецепта'
            )
            return self.form_invalid(form)
        instance.save()
        create_ingredients_amounts(instance, form_data)
        form.save_m2m()
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404('Вы не являетесь автором данного рецепта')

        return super(RecipeUpdateView, self).dispatch(
            request, *args, **kwargs
        )

    def get_success_url(self):
        return reverse('recipe', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})
        context.update({'is_edit': True})

        return context


class RecipeDetailView(DetailView):
    """
    Detail recipe
    """
    model = Recipe
    template_name = 'recipe.html'
    template_name_field = 'recipe'


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete recipe
    """
    model = Recipe
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_object(self, queryset=None):
        recipe = super(RecipeDeleteView, self).get_object()
        if recipe.author != self.request.user:
            raise Http404('Вы не являетесь автором данного рецепта')

        return recipe


class AuthorRecipeListView(RecipeListView):
    """
    Author's recipes
    """

    template_name = 'author.html'

    def get_queryset(self):
        current_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        queryset = Recipe.recipes.filter(author=current_user)

        return get_filters(self.request, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['author'] = author

        return context


class FavoriteListView(RecipeListView):
    """
    Favorite recipes
    """
    template_name = 'favorite.html'

    def get_queryset(self):
        author = self.request.user
        queryset = Recipe.recipes.filter(favorite_recipes__user=author).all()
        return get_filters(self.request, queryset)


class FollowListView(ListView):
    """
    My subscriptions view
    """
    model = Recipe
    template_name = 'subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        authors = User.objects.filter(following__user=user)
        context['authors'] = authors
        favorite_recipes = {}
        for author in authors:
            favorite_recipes[author] = Recipe.recipes.filter(
                author=author
            ).order_by('-pub_date')[:3]
        context['favorite_recipes'] = favorite_recipes
        return context


class PurchaseList(ListView):
    """
    view  Shopping list
    """
    model = Purchase
    template_name = 'purchaselist.html'


def purchaselist_download(request):
    recipes = Recipe.recipes.filter(selected_recipes__user=request.user)
    ingredients = recipes.annotate(
        title=F('ingredients__name'),
        units=F('ingredients__unit')
    ).values('title', 'ingredients__unit').order_by('title').annotate(
        total=Sum('amount_recipes__units')
    )
    response = HttpResponse(content_type='text/text')
    response['Content-Disposition'] = 'attachment; filename="purchaselist.txt"'

    writer = csv.writer(response)
    writer.writerow([f'Список покупок: {request.user.get_full_name()}'])
    writer.writerow([])
    writer.writerow(['Блюда:'])
    for recipe in recipes:
        writer.writerow([recipe.name])
    writer.writerow([])
    writer.writerow(['Ингредиенты:'])
    for ingredient in ingredients:
        if ingredient['title']:
            name = ingredient['title']
            dimension = ingredient['ingredients__unit']
            total = ingredient['total']
            writer.writerow([f'{name} - {total} {dimension}'])

    return response


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
        favorite, created = Favorite.favorite.get_or_create(
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
        removed = Favorite.favorite.filter(
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


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path},
                  status=404
                  )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'misc/403.html', {'path': request.path},
                  status=403
                  )
