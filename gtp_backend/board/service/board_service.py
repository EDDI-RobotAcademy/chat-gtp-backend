from abc import ABC, abstractmethod

class BoardService(ABC):
    @abstractmethod
    def update(self):
        pass


    @abstractmethod
    def get_all_stocks(self):
        pass

    @abstractmethod
    def read_stock(self, ticker):
        pass


