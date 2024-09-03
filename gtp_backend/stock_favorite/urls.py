from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock_favorite.controller.views import FavoriteStocksView

router = DefaultRouter()
router.register(r'favorite_stocks', FavoriteStocksView, basename='favorite_stocks')

urlpatterns = [
    path('', include(router.urls)),
    path('favorite/add', FavoriteStocksView.as_view({'post': 'addFavorite'}), name='favorite-stock-add'),
    path('favorite/list', FavoriteStocksView.as_view({'post': 'get_favorite_stocks'}), name='favorite-stock-list'),
    path('favorite/remove', FavoriteStocksView.as_view({'post': 'removeFavorite'}), name='favorite-stock-remove')
]