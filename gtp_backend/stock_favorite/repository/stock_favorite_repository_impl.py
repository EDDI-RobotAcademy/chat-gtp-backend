from board.entity.models import StockData
from stock_favorite.entity.models import FavoriteStocks
from stock_favorite.repository.stock_favorite_repository import FavoriteStocksRepository

class FavoriteStocksRepositoryImpl(FavoriteStocksRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        from stock_favorite.service.stock_favorite_service_impl import FavoriteStocksServiceImpl
        self.favoriteStocksService = FavoriteStocksServiceImpl.getInstance()

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create(self, email, ticker):
        favorite = FavoriteStocks(email=email, ticker=ticker)
        favorite.save()
        print("Saved favorite: ", favorite)
        return favorite

    def findByEmail(self, email):
        return FavoriteStocks.objects.filter(email=email)

    def delete(self, email, ticker):
        FavoriteStocks.objects.filter(email=email, ticker=ticker).delete()

    def get_favorite_stocks(self, email):
        # FavoriteStocks에서 해당 email의 ticker들을 추출
        tickers = FavoriteStocks.objects.filter(email=email).values_list('ticker', flat=True)

        # 추출한 ticker들을 바탕으로 StockData에서 'name'과 'ticker' 필드를 검색
        favorite_stocks = StockData.objects.filter(ticker__in=tickers).values_list('name', 'ticker')

        print("Favorite stocks: ", favorite_stocks)
        return list(favorite_stocks)

    def find_favorite_tickers_by_email(self, email):
        return list(FavoriteStocks.objects.filter(email=email).values_list('ticker', flat=True))