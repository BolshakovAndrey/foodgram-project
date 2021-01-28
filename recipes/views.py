from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

from recipes.models import Recipe, Tag, User, Purchase
from .forms import RecipeForm
from .util import  get_filters, get_all_tags, create_ingredients_quantity


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


class RecipeCreateView(CreateView):
    """
        Adds a new recipe.
        After validating the form and creating a new recipe,
        the author is redirected to the index page.
    """
    form_class = RecipeForm
    template_name = 'formCreateChangeRecipe.html'
    success_url = 'index'

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
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
        recipe.save()
        create_ingredients_quantity(recipe, form_data)
        form.save_m2m()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})

        return context


class RecipeUpdateView(UpdateView):
    """
    Update recipe
    After validating the form and updating recipe,
    the author is redirected to the recipe page.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = "formCreateChangeRecipe.html"
    fields = ("title", "image", "description", "cook_time")
    template_name_field = "recipe"

    def form_valid(self, form):
        recipe = form.save(commit=False)
        form_data = form.data
        recipe.amount_set.all().delete()
        ingredients = [
            key for key in form_data if key.startswith('nameIngredient_')
        ]
        if not ingredients:
            form.add_error(
                'description',
                'Необходимо указать хотя бы один ингредиент для рецепта'
            )
            return self.form_invalid(form)
        recipe.save()
        create_ingredients_quantity(recipe, form_data)
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


class RecipeDeleteView(DeleteView):
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

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        qs = Recipe.objects.filter(author=user)
        return get_filters(self.request, qs)


def get_context_data(self, **kwargs):
    context = super.get_context_data(**kwargs)
    author = get_object_or_404(User, pk=self.kwargs.get('pk'))
    context['author'] = author


class FavoriteListView(RecipeListView):
    """
    Favorite recipes
    """
    template_name = 'favorite.html'

    def get_queryset(self):
        author = self.request.user
        qs = Recipe.objects.filter(favrecipe__user=author).all()
        return get_filters(self.request, qs)


class FollowListView(ListView):
    """
    My subscriptions view
    """
    model = Recipe
    template_name = 'subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super.get_context_data(**kwargs)
        user = self.request.user
        authors = User.objects.filter(following__user=user)
        context['authors'] = authors
        fav_recipes = {}
        for author in authors:
            fav_recipes[author] = Recipe.objects.filter(
                author=author
            ).order_by('-pub_date')[:3]
        context['fav_recipe'] = fav_recipes
        return context


class PurchaseList(ListView):
    model = Purchase
    template_name = 'purchaselist.html'
