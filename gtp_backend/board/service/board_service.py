from abc import ABC, abstractmethod

class BoardService(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def createBoard(self, boardData):
        pass