import logging
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from pykrx import stock
from board.entity.models import StockData
from board.repository.board_repository import BoardRepository

logger = logging.getLogger(__name__)

class BoardRepositoryImpl(BoardRepository):
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
        logger.info("Updating stock data in repository")

        # db에 데이터가 있을 경우 업데이트 하지 않음
        if StockData.objects.exists():
            print("Stock data already exists in the database. Skipping update.")
            return

        logger.info("Fetching new stock data...")
        ohlcv = stock.get_market_ohlcv("2024030", market="KOSPI")
        tickers = ohlcv.index

        ohlcv.insert(0, 'name', [stock.get_market_ticker_name(ticker) for ticker in tickers])

        data_to_save = []
        for index, row in ohlcv.iterrows():
            data_to_save.append(
                StockData(
                    ticker=index,
                    name=row['name'],
                )
            )

        StockData.objects.bulk_create(data_to_save)

        logger.info("Stock data updated successfully")

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

    @staticmethod
    def get_last_trading_day(date):
        while date.weekday() > 4:  # 0: Monday, 1: Tuesday, ..., 4: Friday, 5: Saturday, 6: Sunday
            date -= timedelta(days=1)
        return date

    def get_realtime_stock_datas(self, ticker: str):
        today = self.get_last_trading_day(datetime.now()).strftime("%Y%m%d")
        yesterday = self.get_last_trading_day(datetime.now() - timedelta(1)).strftime("%Y%m%d")

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
        today = self.get_last_trading_day(datetime.now()).strftime("%Y%m%d")
        yesterday = self.get_last_trading_day(datetime.now() - timedelta(1)).strftime("%Y%m%d")

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

    def search_ticker(self, stockName):
        try:
            stockData = StockData.objects.get(name=stockName)
            print(stockData.ticker)
            return stockData.ticker

        except stockData.DoesNotExist:
            print(f"주식 이름으로 ticker 정보를 찾을 수 없습니다: {stockData}")
            return None
        except Exception as e:
            print(f'주식 이름 검사 중 에러: {e}')
            return None


