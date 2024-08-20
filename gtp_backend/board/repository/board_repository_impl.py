import pandas as pd
from datetime import datetime, time
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pykrx import stock
from board.entity.models import StockData, UpdateLog
from board.repository.board_repository import BoardRepository

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

    def get_last_business_day(self):
        """주말과 공휴일을 제외한 가장 최근의 영업일을 반환"""
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)  # 현재 시간을 KST로 변환

        # 현재 시간이 오후 4시 이후인지 확인
        if now.time() >= time(16, 0):
            return now.date()  # 오늘 날짜를 반환
        else:
            # 현재 시간이 오후 4시 이전이면 가장 최근 영업일을 반환
            last_business_day = now - pd.tseries.offsets.BDay(1)
            return last_business_day.date()

    def update_stock_data(self):
        print("Updating stock data in repository")

        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)
        last_update = UpdateLog.objects.last()

        # 가장 최근의 영업일 계산
        last_business_day = self.get_last_business_day()
        last_business_day_str = last_business_day.strftime('%Y%m%d')

        # 업데이트 필요 여부 판단
        update_required = False

        if last_update:
            last_update_time_kst = last_update.updated_at_kst

            # 마지막 업데이트 시간이 오늘 날짜와 같고, 오후 4시 이후인 경우
            if last_update_time_kst.date() == now_kst.date():
                if last_update_time_kst.time() >= time(16, 0):
                    print("이미 오늘 업데이트가 완료되었습니다.")
                    return
                else:
                    update_required = True
            else:
                update_required = True
        else:
            update_required = True

        if update_required:
            # 가장 최근의 영업일 데이터 삭제
            print("Deleting old stock data...")
            StockData.objects.all().delete()  # 모든 데이터를 삭제

            # KOSPI 시장의 종가 데이터 가져오기
            print("Fetching new stock data...")
            ohlcv = stock.get_market_ohlcv(last_business_day_str, market="KOSPI")
            tickers = ohlcv.index

            # 종목 이름 추가
            ohlcv.insert(0, 'name', [stock.get_market_ticker_name(ticker) for ticker in tickers])

            # 데이터베이스에 저장할 리스트 생성
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

            # 데이터베이스에 저장
            StockData.objects.bulk_create(data_to_save)

            # 마지막 업데이트 시간 기록
            UpdateLog.objects.create()

            print("Stock data updated successfully")
        else:
            print("No update required. The data is already up-to-date.")

    def create(self, boardData):
        board = StockData(**boardData)
        board.save()
        return board

    def get_all_stocks(self):
        return StockData.objects.all()

    def findByTicker(self, ticker):
        try:
            return StockData.objects.get(ticker=ticker)
        except StockData.DoesNotExist:
            return None

    def get_all_stocks_paginated(self, page, per_page):
        """
        주식 데이터를 페이지네이션하여 가져오는 메서드
        :param page: 가져올 페이지 번호
        :param per_page: 페이지당 아이템 수
        :return: 페이지네이션된 주식 데이터
        """
        all_stocks = StockData.objects.all()
        paginator = Paginator(all_stocks, per_page)  # Paginator 객체 생성
        try:
            stocks = paginator.page(page)
        except EmptyPage:
            stocks = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            stocks = paginator.page(1)

        return stocks