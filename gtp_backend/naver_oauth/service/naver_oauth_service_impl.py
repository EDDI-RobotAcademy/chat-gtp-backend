from gtp_backend import settings


import requests

from naver_oauth.service.naver_oauth_service import NaverOauthService


class NaverOauthServiceImpl(NaverOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.NAVER['LOGIN_URL']
            cls.__instance.clientId = settings.NAVER['CLIENT_ID']
            cls.__instance.redirectUri = settings.NAVER['REDIRECT_URI']
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def naverLoginAddress(self):
        print("naverLoginAddress()")
        return (f"{self.loginUrl}?"
                f"&response_type=code&client_id={self.clientId}&state=1234&redirect_uri={self.redirectUri}")

