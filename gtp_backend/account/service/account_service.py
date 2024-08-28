from abc import ABC, abstractmethod


class AccountService(ABC):
    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def checkNicknameDuplication(self, nickname):
        pass

    @abstractmethod
    def checkPasswordDuplication(self, email,password):
        pass

    @abstractmethod
    def registerAccount(self,nickname,password,salt,email,loginType):
        pass

    @abstractmethod
    def findAccountByEmail(self, email):
        pass

    @abstractmethod
    def findAccountById(self, accountId):
        pass