import pandas as pd
from datetime import datetime, time
import pytz
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

        # 주말 및 공휴일을 제외한 가장 최근의 영업일 계산
        last_business_day = self.get_last_business_day()
        last_business_day_str = last_business_day.strftime('%Y%m%d')

        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)
        last_update = UpdateLog.objects.last()

        update_required = False

        if last_update:
            last_update_time_kst = last_update.updated_at_kst

            # 마지막 업데이트 날짜와 현재 날짜 비교
            if last_update_time_kst.date() < now_kst.date():
                update_required = True
            elif last_update_time_kst.date() == now_kst.date():
                # 오늘 이미 오후 4시 이후에 업데이트가 완료된 경우
                if now_kst.time() < time(16, 0) and last_update_time_kst.time() >= time(16, 0):
                    print("이미 오늘 업데이트가 완료되었습니다.")
                    return
                else:
                    update_required = True
        else:
            # 업데이트 로그가 없는 경우 (초기 상태)
            update_required = True

        if update_required:
            # 업데이트가 필요한 경우 데이터베이스에서 전날 데이터 삭제
            print("Deleting old stock data...")
            StockData.objects.filter(date=last_business_day).delete()

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