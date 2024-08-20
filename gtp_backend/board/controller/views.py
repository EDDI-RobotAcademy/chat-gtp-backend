from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from pykrx import stock
from board.entity.models import StockData
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

    def stock_detail(self, request, pk=None):
        stock = self.stockService.read_stock(pk)
        serializer = StockDataSerializer(stock)
        return Response(serializer.data)

    def get_paginated_stocks(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        search_query = request.GET.get('search', '')

        # 검색 조건 적용
        stocks_query = StockData.objects.all()
        if search_query:
            stocks_query = stocks_query.filter(
                Q(name__icontains=search_query) |
                Q(ticker__icontains=search_query)
            )

        # 총 아이템 수 계산 (필터링된 결과 기준)
        total_items = stocks_query.count()

        # 페이지네이션 처리
        start = (page - 1) * size
        end = start + size

        # 필터링된 결과에서 페이지네이션 적용
        paginated_stocks_query = stocks_query[start:end]

        # 응답 데이터 구성
        data = {
            'stocks': list(paginated_stocks_query.values()),
            'totalItems': total_items,
            'currentPage': page,
            'totalPages': (total_items + size - 1) // size  # 전체 페이지 수 계산
        }

        return JsonResponse(data)

    def get_stock_data(self, request, ticker, start_date, end_date):
        df = stock.get_market_ohlcv(start_date, end_date, ticker)
        df = df.reset_index()  # 인덱스를 초기화하여 날짜를 컬럼으로 변환
        df['날짜'] = df['날짜'].apply(lambda x: x.strftime('%Y-%m-%d'))  # 날짜 형식 변환
        data = df.to_dict(orient='records')  # 데이터를 딕셔너리 형식으로 변환
        return Response(data)