from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path("<slug>/edit/", views.RecipeUpdateView.as_view(), name="recipe_update"),
    path("<slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("<slug>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path('new', views.RecipeCreateView.as_view(), name='recipe_create'),
]
