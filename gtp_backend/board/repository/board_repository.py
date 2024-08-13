from abc import ABC, abstractmethod

class BoardRepository(ABC):
    @abstractmethod
    def update_stock_data(self):
        pass
    @abstractmethod
    def create(self, boardData):
        pass