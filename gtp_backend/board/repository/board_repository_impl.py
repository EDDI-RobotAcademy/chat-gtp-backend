import logging
from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from django.core.paginator import Paginator
from django.db.models import Q
from pykrx import stock
from board.entity.models import StockData, UpdateLog

logger = logging.getLogger(__name__)

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


    def get_last_business_day(self):
        """주말과 공휴일을 제외한 가장 최근의 영업일을 반환"""
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)  # 현재 시간을 KST로 변환

        if now.time() >= time(16, 0):
            return now.date()  # 오늘 날짜를 반환
        else:
            # 현재 시간이 오후 4시 이전이면 가장 최근 영업일을 반환
            last_business_day = now - pd.tseries.offsets.BDay(1)
            return last_business_day.date()

    def update_stock_data(self):
        logger.info("Updating stock data in repository")

        # 주말 및 공휴일을 제외한 가장 최근의 영업일 계산
        last_business_day = self.get_last_business_day()
        last_business_day_str = last_business_day.strftime('%Y%m%d')

        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)
        last_update = UpdateLog.objects.last()

        update_required = False

        if last_update:
            last_update_time_kst = last_update.updated_at_kst

            if last_update_time_kst.date() == now_kst.date():
                if now_kst.time() < time(16, 0) and last_update_time_kst.time() >= time(16, 0):
                    logger.info("이미 오늘 업데이트가 완료되었습니다.")
                    return
            else:
                update_required = True
        else:
            update_required = True

        if update_required:
            try:
                logger.info("Deleting old stock data...")
                StockData.objects.filter(date=last_business_day).delete()

                logger.info("Fetching new stock data...")
                ohlcv = stock.get_market_ohlcv(last_business_day_str, market="KOSPI")
                tickers = ohlcv.index

                ohlcv.insert(0, 'name', [stock.get_market_ticker_name(ticker) for ticker in tickers])

                data_to_save = []
                for index, row in ohlcv.iterrows():
                    data_to_save.append(
                        StockData(
                            ticker=index,
                            name=row['name'],
                            date=last_business_day,
                            open=row['시가'],
                            high=row['고가'],
                            low=row['저가'],
                            close=row['종가'],
                            volume=row['거래량']
                        )
                    )

                StockData.objects.bulk_create(data_to_save)

                UpdateLog.objects.create()

                logger.info("Stock data updated successfully")
            except Exception as e:
                logger.error("Error updating stock data", exc_info=True)
        else:
            logger.info("No update required. The data is already up-to-date.")
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
