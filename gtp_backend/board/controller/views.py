from rest_framework.response import Response
from rest_framework import viewsets
from board.service.board_service_impl import BoardServiceImpl

class StockView(viewsets.ViewSet):
    stockService = BoardServiceImpl.getInstance()

    def update_stock_data(self, *args, **kwargs):
        print("Updating stock data...")
        self.stockService.update()
        return Response({"status": "stock data updated"})