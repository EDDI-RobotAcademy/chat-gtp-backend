from abc import ABC, abstractmethod


class ProfileRepository(ABC):
    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def findByNickname(self, Nickname):
        pass

    @abstractmethod
    def findByPassword(self,password):
        pass

    @abstractmethod
    def create(self, nickname,password,email, account):
        pass