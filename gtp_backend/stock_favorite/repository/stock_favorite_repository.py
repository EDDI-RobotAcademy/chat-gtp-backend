from abc import ABC, abstractmethod

class FavoriteStocksRepository(ABC):
    @abstractmethod
    def create(self, email, ticker):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def delete(self, email, ticker):
        pass

    @abstractmethod
    def get_favorite_stocks(self, email):
        pass