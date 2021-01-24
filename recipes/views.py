from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

from recipes.models import Recipe
from .forms import RecipeForm
from .utils import save_recipe, get_ingredients_from_form


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/indexAuth.html'
    paginate_by = 6

    def get_queryset(self):
        tags = self.request.GET.getlist('tag', '')
        queryset = Recipe.recipes.filter_by_tags(
            tags).select_related('author').prefetch_related('tag').all()
        return queryset


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    success_url = 'index'

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        form_data = form.data

        recipe.save()
        save_recipe(
            ingredients=get_ingredients_from_form(form_data),
            recipe=recipe)
        form.save_m2m()
        return redirect(self.success_url)


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "recipes/formChangeRecipe.html"
    fields = ("title", "image", "description", "cook_time")
    template_name_field = "recipe"


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/singlePage.html'
    template_name_field = "recipe"


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('index_view')

    def get_object(self, queryset=None):
        instance = super(RecipeDeleteView, self).get_object()
        if instance.author != self.request.user:
            raise Http404('Вы не являетесь автором данного рецепта')

        return instance
