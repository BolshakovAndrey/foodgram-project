from django.urls import path

from recipes import views
from recipes.views import (FavoriteView, GetIngredientsView, PurchasesView,
                           SubscribeView, purchaselist_download)

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="edit_recipe"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="delete_recipe"),
    path('new', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('ingredients/', GetIngredientsView.as_view(), name='get_ingredients'),
    path('author/<pk>', views.AuthorRecipeListView.as_view(), name='author'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('favorites', FavoriteView.as_view(), name='add_favorite'),
    path('favorites/<int:recipe_id>', PurchasesView.as_view(), name='remove_favorites'),
    path('purchaselist/', views.PurchaseList.as_view(), name='purchaselist'),
    path('purchases', PurchasesView.as_view(), name='purchases'),
    path('shoplist/download/', purchaselist_download, name='purchaselist_download'),
    path('purchases/<int:recipe_id>', PurchasesView.as_view(), name='remove_purchases'),
    path('subscriptions/', views.FollowListView.as_view(), name='subscriptions'),
    path('subscriptions', SubscribeView.as_view(), name='add_subscription'),
    path('subscriptions/<int:author_id>', SubscribeView.as_view(), name='remove_subscriptions')
]
