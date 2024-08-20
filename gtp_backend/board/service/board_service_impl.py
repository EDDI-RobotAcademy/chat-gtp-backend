from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService

class BoardServiceImpl(BoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__boardRepository = BoardRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def update(self):
        print("BoardServiceImpl update called")
        self.__boardRepository.update_stock_data()


    def get_all_stocks(self):
        return self.__boardRepository.get_all_stocks()

    def read_stock(self, ticker):
        return self.__boardRepository.findByTicker(ticker)

    def get_stocks_paginated(self, page, per_page):
        return self.__boardRepository.get_all_stocks_paginated(page, per_page)