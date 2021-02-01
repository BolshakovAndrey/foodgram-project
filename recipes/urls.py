from django.urls import path

from recipes import views
from recipes.views import purchaselist_download

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="edit_recipe"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="delete_recipe"),
    path('new', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('author/<pk>', views.AuthorRecipeListView.as_view(), name='author'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('subscriptions/', views.FollowListView.as_view(), name='subscriptions'),
    path('purchaselist/', views.PurchaseList.as_view(), name='purchaselist'),
    path('shoplist/download/', purchaselist_download, name='purchaselist_download'),
]
