from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.controller.views import StockView

router = DefaultRouter()
router.register(r'board', StockView, basename='board')

urlpatterns = [
    path("", include(router.urls)),
    path("update_stock_data", StockView.as_view({"post": "update_stock_data"}), name='board-list'),
    path('register', StockView.as_view({'post': 'create'}), name='board-register'),
]