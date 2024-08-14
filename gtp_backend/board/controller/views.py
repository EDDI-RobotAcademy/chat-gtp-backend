from rest_framework.response import Response
from rest_framework import viewsets

from board.serializers import StockDataSerializer
from board.service.board_service_impl import BoardServiceImpl

class StockView(viewsets.ViewSet):
    stockService = BoardServiceImpl.getInstance()

    def update_stock_data(self, *args, **kwargs):
        print("Updating stock data...")
        self.stockService.update()
        return Response({"status": "stock data updated"})

    def get_all_stocks(self, *args, **kwargs):
        stocks = self.stockService.get_all_stocks()
        serializer = StockDataSerializer(stocks, many=True)
        return Response(serializer.data)

    def get_stock(self, request, pk=None):
        stock = self.stockService.read_stock(pk)
        serializer = StockDataSerializer(stock)
        return Response(serializer.data)