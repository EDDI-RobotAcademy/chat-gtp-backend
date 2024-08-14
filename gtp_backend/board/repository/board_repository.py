from abc import ABC, abstractmethod



class BoardRepository(ABC):
    @abstractmethod
    def update_stock_data(self):
        pass
    @abstractmethod
    def create(self, boardData):
        pass

    @abstractmethod
    def get_all_stocks(self):
        pass

    @abstractmethod
    def findByTicker(self, ticker):
        pass