from abc import ABC, abstractmethod
class GoogleOauthService(ABC):
    @abstractmethod
    def googleLoginAddress(self):
        pass

    @abstractmethod
    def requestGoogleAccessToken(self, GoogleAuthCode):
        pass
