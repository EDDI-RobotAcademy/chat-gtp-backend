from rest_framework import serializers
from board.entity.models import StockData, UpdateLog

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['id', 'ticker', 'name', 'date', 'open', 'high', 'low', 'close', 'volume', 'updated_at']
        read_only_fields = ['updated_at']  # updated_at은 자동으로 설정되므로 읽기 전용으로 설정


class UpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateLog
        fields = ['updated_at']
        read_only_fields = ['updated_at']
