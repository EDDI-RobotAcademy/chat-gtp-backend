from rest_framework import serializers
from board.entity.models import StockData

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['id', 'ticker', 'name', 'updated_at']
        read_only_fields = ['updated_at']  # updated_at은 자동으로 설정되므로 읽기 전용으로 설정
