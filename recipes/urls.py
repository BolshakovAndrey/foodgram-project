from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path("<slug>/edit/", views.RecipeUpdateView.as_view(), name="update"),
    path("<slug>/", views.RecipeDetailView.as_view(), name="detail"),
    path("<slug>/delete/", views.RecipeDeleteView.as_view(), name="delete"),
    path('new', views.RecipeCreateView.as_view(), name='create'),
    path('author/<pk>', views.AuthorRecipeListView.as_view, name='author'),
    path('favorites/', views.FavoriteListView.as_view, name='favorites'),
    path('subscriptions/', views.FollowListView.as_view, name='subscriptions'),
    path('purchaselist/', views.PurchaseList.as_view, name='purchaselist')
]
