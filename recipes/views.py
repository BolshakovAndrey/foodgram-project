import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

from recipes.models import Recipe, Tag, User, Purchase
from .forms import RecipeForm
from .util import get_filters, get_all_tags, create_ingredients_amounts


class RecipeListView(ListView):
    """
    Main page with recipes
    """
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'index.html'
    paginate_by = 6
    template_name_field = "recipes"

    def get_queryset(self):
        qs = super().get_queryset()
        return get_filters(self.request, qs)

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
    template_name = "formCreateChangeRecipe.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        form_data = form.data
        instance.amount_set.all().delete()
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
    template_name_field = "recipe"


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
        qs = Recipe.objects.filter(author=current_user)

        return get_filters(self.request, qs)

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
        qs = Recipe.objects.filter(favorite_recipe__user=author).all()
        return get_filters(self.request, qs)


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
            favorite_recipes[author] = Recipe.objects.filter(
                author=author
            ).order_by('-pub_date')[:3]
        context['favorite_recipes'] = favorite_recipes
        return context


class PurchaseList(ListView):
    model = Purchase
    template_name = 'purchaselist.html'


def purchaselist_download(request):
    recipes = Recipe.objects.filter(selected_recipes__user=request.user)
    ingredients = recipes.annotate(
        title=F('amount__ingredient__name'),
        units=F('amount__ingredient__unit')
    ).values('title', 'units').order_by('title').annotate(
        total=Sum('amount__units')
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
            dimension = ingredient['units']
            total = ingredient['total']
            writer.writerow([f'{name} - {total} {dimension}'])

    return response