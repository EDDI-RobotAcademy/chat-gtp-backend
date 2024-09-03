from board.service.board_service import BoardService
from board.repository.board_repository_impl import BoardRepositoryImpl
from stock_favorite.repository.stock_favorite_repository_impl import FavoriteStocksRepositoryImpl


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
        self.__boardRepository.update_stock_data()

    def read_stock(self, ticker):
        return self.__boardRepository.findByTicker(ticker)

    def get_paginated_stocks(self, page, size, search_query, email=None):
        return self.__boardRepository.get_paginated_stocks(page, size, search_query, email)

    def get_realtime_stock_data(self, ticker, email):
        return self.__boardRepository.get_realtime_stock_data(ticker, email)

    def search_ticker(self, stockName):
        return self.__boardRepository.search_ticker(stockName)



