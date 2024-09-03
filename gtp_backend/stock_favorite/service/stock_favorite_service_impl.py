from account.repository.profile_repository_impl import ProfileRepositoryImpl
from stock_favorite.repository.stock_favorite_repository_impl import FavoriteStocksRepositoryImpl
from stock_favorite.service.stock_favorite_service import FavoriteStocksService

class FavoriteStocksServiceImpl(FavoriteStocksService):
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

    def __init__(self):
        self.favoriteStocksRepository = FavoriteStocksRepositoryImpl.getInstance()
        self.profileRepository = ProfileRepositoryImpl.getInstance()

    def addFavorite(self, email, ticker):
        if email is None or ticker is None:
            raise ValueError("Email and Ticker must not be None")

        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            raise ValueError("Profile not found for the given email")

        return self.favoriteStocksRepository.create(email, ticker)

    def getFavorites(self, email):
        if email is None:
            raise ValueError("Email must not be None")

        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            raise ValueError("Profile not found for the given email")

        return self.favoriteStocksRepository.findByEmail(email)

    def removeFavorite(self, email, ticker):
        if email is None or ticker is None:
            raise ValueError("Email and Ticker must not be None")

        self.favoriteStocksRepository.delete(email, ticker)

    def isFavorite(self, email, ticker):
        if email is None or ticker is None:
            raise ValueError("Email and Ticker must not be None")

        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            raise ValueError("Profile not found for the given email")

        return self.favoriteStocksRepository.findByEmail(email).filter(ticker=ticker).exists()

    def get_favorite_stocks(self, email):
        return self.favoriteStocksRepository.get_favorite_stocks(email)