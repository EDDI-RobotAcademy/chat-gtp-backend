from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kis_trading.controller.trading_controller import TradingView

router = DefaultRouter()
router.register(r'trading', TradingView, basename='trading')

urlpatterns = [
    path('', include(router.urls)),
    path('order', TradingView.as_view({'post': 'order_stock'}), name='buy-stock'),
    path('list', TradingView.as_view({'post': 'get_my_complete'}), name='list-my-stock'),
    # path('/list', FavoriteStocksView.as_view({'post': 'get_favorite_stocks'}), name='favorite-stock-list'),
    # path('favorite/remove', FavoriteStocksView.as_view({'post': 'removeFavorite'}), name='favorite-stock-remove')
]