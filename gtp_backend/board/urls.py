from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.controller.views import StockView

router = DefaultRouter()
router.register(r'board', StockView, basename='board')

urlpatterns = [
    path("", include(router.urls)),
    path('get-stock/<str:pk>', StockView.as_view({'get': 'stock_detail'}), name='board-read'),
    path('stock/<str:ticker>/<str:start_date>/<str:end_date>/', StockView.as_view({'get': 'get_stock_data'}), name='board-stock-data'),
    path('stocks', StockView.as_view({'get': 'get_paginated_stocks'}), name='get_paginated_stocks'),
    path('stocks/realtime/<str:ticker>/', StockView.as_view({'get': 'get_realtime_stock_data'}), name='stock-realtime-data'),
    path('search-ticker',StockView.as_view({'post':'searchTicker'}),name='search-ticker')
]

