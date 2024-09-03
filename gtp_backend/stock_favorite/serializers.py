from rest_framework import serializers
from stock_favorite.entity.models import FavoriteStocks

class FavoriteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteStocks
        fields = '__all__'