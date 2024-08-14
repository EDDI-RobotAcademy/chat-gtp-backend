from account.repository.account_repository_impl import AccountRepositoryImpl
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.service.account_service import AccountService


class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__profileRepository = ProfileRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def checkEmailDuplication(self, email):
        profile = self.__profileRepository.findByEmail(email)
        return profile is not None

    def checkNicknameDuplication(self, nickname):
        account = self.__profileRepository.findByNickname(nickname)
        return account is not None

    def checkPasswordDuplication(self, email,password):
        account = self.__profileRepository.findByPassword(email,password)
        return account

    def registerAccount(self,nickname,password,email,loginType):
        account = self.__accountRepository.create(loginType)
        return self.__profileRepository.create(nickname, password, email, account)

    def findAccountByEmail(self, email):
        return self.__profileRepository.findByEmail(email)

    def findAccountById(self, accountId):
        return self.__accountRepository.findById(accountId)