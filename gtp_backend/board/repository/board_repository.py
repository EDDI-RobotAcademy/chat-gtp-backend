from abc import ABC, abstractmethod


class BoardRepository(ABC):
    @abstractmethod
    def update_stock_data(self):
        pass

    @abstractmethod
    def findByTicker(self, ticker):
        pass

    @abstractmethod
    def get_paginated_stocks(self, page, size, search_query, email):
        pass

    @abstractmethod
    def get_realtime_stock_data(self, ticker):
        pass

    @abstractmethod
    def search_ticker(self,stockName):
        pass