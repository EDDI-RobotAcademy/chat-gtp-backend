from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from pykrx import stock

from board.entity.models import StockData

class BoardRepositoryImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def update_stock_data(self):
        pass  # 업데이트 로직 구현

    def create(self, boardData):
        pass  # 생성 로직 구현

    def get_all_stocks(self):
        return list(StockData.objects.all().values())

    def findByTicker(self, ticker):
        return StockData.objects.filter(ticker=ticker).first()

    def get_all_stocks_paginated(self, page, per_page):
        all_stocks = StockData.objects.all().order_by('id')  # 정렬 추가
        paginator = Paginator(all_stocks, per_page)
        paginated_stocks = paginator.get_page(page)
        return list(paginated_stocks.object_list), paginator.count

    def get_paginated_stocks(self, page, size, search_query):
        query = StockData.objects.all()
        if search_query:
            query = query.filter(
                Q(name__icontains=search_query) | Q(ticker__icontains=search_query)
            )

        query = query.order_by('id')  # 정렬 추가

        paginator = Paginator(query, size)
        paginated_stocks = paginator.get_page(page)
        stocks = list(paginated_stocks.object_list.values())

        for stock in stocks:
            realtime_data = self.get_realtime_stock_datas(stock['ticker'])
            if realtime_data:
                stock.update(realtime_data)

        total_pages = paginator.num_pages
        total_items = paginator.count

        return stocks, total_items, total_pages

    def get_realtime_stock_datas(self, ticker: str):
        today = datetime.now().strftime("%Y%m%d")
        yesterday = (datetime.now() - timedelta(1)).strftime("%Y%m%d")

        try:
            # 오늘 날짜의 종가
            today_data = stock.get_market_ohlcv_by_date(today, today, ticker)
            if today_data.empty:
                return None

            today_open = today_data.iloc[-1]['시가']
            today_high = today_data.iloc[-1]['고가']
            today_low = today_data.iloc[-1]['저가']
            today_close = today_data.iloc[-1]['종가']
            today_volume = today_data.iloc[-1]['거래량']


            # 전날 날짜의 종가
            yesterday_data = stock.get_market_ohlcv_by_date(yesterday, yesterday, ticker)
            if yesterday_data.empty:
                return None

            yesterday_close = yesterday_data.iloc[-1]['종가']

            # 등락률 계산
            price_change = today_close - yesterday_close
            percentage_change = (price_change / yesterday_close) * 100

            return {
                "open": today_open,
                "high": today_high,
                "low": today_low,
                "close": today_close,
                "volume": today_volume,
                "priceChange": price_change,
                "percentageChange": percentage_change
            }
        except Exception as e:
            print(f"Error fetching real-time data for {ticker}: {e}")
            return None


    def get_realtime_stock_data(self, ticker: str):
        today = datetime.now().strftime("%Y%m%d")
        yesterday = (datetime.now() - timedelta(1)).strftime("%Y%m%d")

        try:

            # 오늘 날짜의 종가
            today_data = stock.get_market_ohlcv_by_date(today, today, ticker)
            if today_data.empty:
                return None

            today_open = today_data.iloc[-1]['시가']
            today_high = today_data.iloc[-1]['고가']
            today_low = today_data.iloc[-1]['저가']
            today_close = today_data.iloc[-1]['종가']
            today_volume = today_data.iloc[-1]['거래량']

            # 전날 날짜의 종가
            yesterday_data = stock.get_market_ohlcv_by_date(yesterday, yesterday, ticker)
            if yesterday_data.empty:
                return None

            yesterday_close = yesterday_data.iloc[-1]['종가']

            # 등락률 계산
            price_change = today_close - yesterday_close
            percentage_change = (price_change / yesterday_close) * 100

            return {
                "open": today_open,
                "high": today_high,
                "low": today_low,
                "close": today_close,
                "volume": today_volume,
                "priceChange": price_change,
                "percentageChange": percentage_change
            }
        except Exception as e:
            print(f"Error fetching real-time data for {ticker}: {e}")
            return None
