from abc import ABC, abstractmethod
class NaverOauthService(ABC):
    @abstractmethod
    def naverLoginAddress(self):
        pass

    @abstractmethod
    def requestNaverAccessToken(self,naverCode):
        pass

    @abstractmethod
    def requestUserInfo(self,accessToken):
        pass