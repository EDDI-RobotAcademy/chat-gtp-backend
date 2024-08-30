from abc import ABC, abstractmethod


class BoardService(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read_stock(self, ticker):
        pass

    @abstractmethod
    def get_paginated_stocks(self, page, size, search_query):
        pass

    @abstractmethod
    def get_realtime_stock_data(self, ticker):
        pass

