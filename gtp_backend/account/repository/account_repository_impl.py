from account.entity.account import Account
from account.entity.account_login_type import AccountLoginType
from account.repository.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, loginType):
        loginTypeEntity, _ = AccountLoginType.objects.get_or_create(loginType=loginType)

        account = Account.objects.create(loginType=loginTypeEntity)
        return account

    def findById(self, accountId):
        try:
            account = Account.objects.get(accountId=accountId)
            return account
        except Account.DoesNotExist:
            print(f"아이디로 계정 정보를 찾을 수 없습니다: {accountId}")
            return None
        except Exception as e:
            print(f'아이디 중복 검사 중 에러: {e}')
            return None