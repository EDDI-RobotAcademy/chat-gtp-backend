from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
from pykrx import stock
from board.entity.models import StockData
from board.serializers import StockDataSerializer
from board.service.board_service_impl import BoardServiceImpl

class StockView(viewsets.ViewSet):
    stockService = BoardServiceImpl.getInstance()

    # 주식 데이터(ticker, 주식 종목) 업데이트
    def update_stock_data(self, *args, **kwargs):
        print("Updating stock data...")
        self.stockService.update()
        return Response({"status": "stock data updated"})

    # detail 페이지 조회
    def stock_detail(self, request, pk=None):
        stock = self.stockService.read_stock(pk)
        serializer = StockDataSerializer(stock)
        return Response(serializer.data)

    # 주식 종목 페이지네이션
    def get_paginated_stocks(self, request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        search_query = request.GET.get('search', '')
        email = request.GET.get('email', None)  # email 추가

        stocks, total_items, total_pages = self.stockService.get_paginated_stocks(page, size, search_query, email)
        data = {
            'stocks': stocks,
            'totalItems': total_items,
            'currentPage': page,
            'searchQuery': search_query,
            'totalPages': total_pages
        }

        return JsonResponse(data)

    # 주식 차트 그리기 위한 데이터 조회
    def get_stock_data(self, request, ticker, start_date, end_date):
        df = stock.get_market_ohlcv(start_date, end_date, ticker)
        df = df.reset_index()  # 인덱스를 초기화하여 날짜를 컬럼으로 변환
        df['날짜'] = df['날짜'].apply(lambda x: x.strftime('%Y-%m-%d'))  # 날짜 형식 변환
        data = df.to_dict(orient='records')  # 데이터를 딕셔너리 형식으로 변환
        return Response(data)

    # 실시간 주식 데이터 조회
    def get_realtime_stock_data(self, request, ticker):
        email = request.GET.get('email', None)
        print("email: ", email)
        # 종목명 조회
        stock = get_object_or_404(StockData, ticker=ticker)
        print(stock)
        # 외부 API로부터 실시간 데이터 가져오기
        realtime_data = self.stockService.get_realtime_stock_data(ticker, email)

        if realtime_data is not None:
            # 종목명 추가
            realtime_data["name"] = stock.name
            return Response(realtime_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch real-time data"}, status=status.HTTP_404_NOT_FOUND)

    def searchTicker(self,request):
        stockName = request.data.get("stockName")

        ticker = self.stockService.search_ticker(stockName['stockName'])

        if ticker is not None:
            return Response(ticker,status=status.HTTP_200_OK)
        else:
            return Response({"error": "맞는 종목이 존재하지 않습니다"},status=status.HTTP_404_NOT_FOUND)

