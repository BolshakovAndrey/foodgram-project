from django.urls import path

from recipes.views import (AuthorRecipeListView, FavoriteListView,
                           FavoriteView, FollowListView, GetIngredientsView,
                           PurchaseList, PurchasesView, RecipeCreateView,
                           RecipeDeleteView, RecipeDetailView, RecipeListView,
                           RecipeUpdateView, SubscribeView,
                           purchaselist_download)

urlpatterns = [
    # recipes
    path('', RecipeListView.as_view(), name='index'),
    path('<int:pk>/edit/', RecipeUpdateView.as_view(), name='edit_recipe'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe'),
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='delete_recipe'),
    path('new/', RecipeCreateView.as_view(), name='new_recipe'),
    path('ingredients/', GetIngredientsView.as_view(), name='get_ingredients'),
    path('author/<pk>/', AuthorRecipeListView.as_view(), name='author'),
    # favorites
    path('favoriteslist/', FavoriteListView.as_view(), name='favorites'),
    path('favorites/', FavoriteView.as_view(), name='add_favorite'),
    path('favorites/<int:recipe_id>/',
         FavoriteView.as_view(), name='remove_favorites'),
    # subscriptions
    path('subscriptionslist/', FollowListView.as_view(), name='subscriptions'),
    path('subscriptions/', SubscribeView.as_view(), name='add_subscription'),
    path('subscriptions/<int:author_id>/',
         SubscribeView.as_view(), name='remove_subscriptions'),
    # purchases
    path('purchaselist/', PurchaseList.as_view(), name='purchaselist'),
    path('purchases/',
         PurchasesView.as_view(), name='add-purchases'),
    path('purchases/<int:recipe_id>/',
         PurchasesView.as_view(), name='remove_purchases'),
    path('shoplist/download/',
         purchaselist_download, name='purchaselist_download'),
]
