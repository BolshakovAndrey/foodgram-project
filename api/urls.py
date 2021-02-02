from django.urls import path

from .views import (FavoriteView, GetIngredientsView, PurchasesView,
                    SubscribeView)

urlpatterns = [
    path('favorites', FavoriteView.as_view(),
         name='add_favorite'),
    path('favorites/<int:recipe_id>',
         FavoriteView.as_view(),
         name='remove_favorites'),
    path('ingredients/', GetIngredientsView.as_view(),
         name='get_ingredients'),
    path('purchases', PurchasesView.as_view(),
         name='purchases'),
    path(
        'purchases/<int:recipe_id>', PurchasesView.as_view(),
        name='remove_purchases'),
    path('subscriptions', SubscribeView.as_view(),
         name='add_subscription'),
    path('subscriptions/<int:author_id>', SubscribeView.as_view(),
         name='remove_subscriptions')
]
