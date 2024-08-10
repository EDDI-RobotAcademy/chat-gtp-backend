from gtp_backend import settings
from google_oauth.service.google_oauth_service import GoogleOauthService

import requests


class GoogleOauthServiceImpl(GoogleOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.GOOGLE['LOGIN_URL']
            cls.__instance.clientId = settings.GOOGLE['CLIENT_ID']
            cls.__instance.clientSecret = settings.GOOGLE['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GOOGLE['TOKEN_REQUEST_URI']
            cls.__instance.userEmailRequestUri = settings.GOOGLE['USEREMAIL_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GOOGLE['USERINFO_REQUEST_URI']
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def googleLoginAddress(self):
        print("googleLoginAddress()")
        return (f"{self.loginUrl}/oauth2/v2/auth?"
                f"client_id={self.clientId}&redirect_uri={self.redirectUri}"
                f"&response_type=code&scope=email%20profile%20openid")

    def requestGoogleAccessToken(self, googleAuthCode):
        print("requestAccessToken()")
        accessTokenRequestForm = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'code': googleAuthCode,
            'client_secret': self.clientSecret
        }
        print(accessTokenRequestForm)
        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForm)
        return response.json()

    def requestUserEmail(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.post(self.userEmailRequestUri, headers=headers)
        return response.json()

    def requestUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.post(self.userInfoRequestUri, headers=headers)
        return response.json()


