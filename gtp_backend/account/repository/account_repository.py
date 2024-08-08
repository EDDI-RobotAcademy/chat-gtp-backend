from abc import ABC, abstractmethod


class AccountRepository(ABC):
    @abstractmethod
    def create(self, id,loginType,password):
        pass

    @abstractmethod
    def findById(self, id):
        pass