from abc import ABC, abstractmethod

class FavoriteStocksService(ABC):
    @abstractmethod
    def addFavorite(self, email, ticker):
        pass

    @abstractmethod
    def getFavorites(self, email):
        pass

    @abstractmethod
    def removeFavorite(self, email, ticker):
        pass

    @abstractmethod
    def isFavorite(self, email, ticker):
        pass

    @abstractmethod
    def get_favorite_stocks(self,email):
        pass

