from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.controller.views import StockView

router = DefaultRouter()
router.register(r'board', StockView, basename='board')

urlpatterns = [
    path("", include(router.urls)),
    path("update-stock-data", StockView.as_view({"post": "update_stock_data"}), name='board-update'),
    path('get-all-stocks', StockView.as_view({'get': 'get_all_stocks'}), name='board-list'),
    path('get-stock/<str:pk>', StockView.as_view({'get': 'get_stock'}), name='board-read')
]