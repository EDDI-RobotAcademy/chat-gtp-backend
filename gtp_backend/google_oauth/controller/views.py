import uuid
from urllib import parse

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from google_oauth.serializer.google_oauth_access_token_serializer import GoogleOauthAccessTokenSerializer
from google_oauth.serializer.google_oauth_url_serializer import GoogleOauthUrlSerializer
from google_oauth.service.google_oauth_service_impl import GoogleOauthServiceImpl
from google_oauth.service.redis_service_impl import RedisServiceImpl


class GoogleOauthView(viewsets.ViewSet):
    googleOauthService = GoogleOauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()

    def googleOauthURI(self, request):
        url = self.googleOauthService.googleLoginAddress()
        print(f"url:", url)
        serializer = GoogleOauthUrlSerializer(data={ 'url': url })
        serializer.is_valid(raise_exception=True)
        print(f"validated_data: {serializer.validated_data}")
        return Response(serializer.validated_data)

    def googleAccessTokenURI(self, request):
        serializer = GoogleOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        try:
            accessToken = self.googleOauthService.requestGoogleAccessToken(code)
            print(f"accessToken: {accessToken}")
            return JsonResponse({'accessToken': accessToken})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def googleUserEmailURI(self, request):
        gooogleAccessToken = request.data.get('access_token')
        print(f'googleOauthService: {gooogleAccessToken}')

        try:
            user_info_email = self.googleOauthService.requestUserEmail(gooogleAccessToken)
            return JsonResponse({'user_info_email': user_info_email})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def googleUserInfoURI(self, request):
        gooogleAccessToken = request.data.get('access_token')
        print(f'googleOauthService: {gooogleAccessToken}')

        try:
            user_info = self.googleOauthService.requestUserInfo(gooogleAccessToken)
            return JsonResponse({'user_info': user_info})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def redisGoogleAccessToken(self, request):
        try:
            email = request.data.get('email')
            access_token = request.data.get('googleAccessToken')
            print(f"redisAccessToken -> email: {email}")

            account = self.accountService.findAccountByEmail(email)
            if not account:
                return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

            userToken = str(uuid.uuid4())
            self.redisService.store_access_token(account.id, userToken)
            accountId = self.redisService.getValueByKey(userToken)
            print(f"accountId: {accountId}")

            return Response({ 'userToken': userToken }, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error storing access token in Redis:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def dropRedisTokenForLogout(self, request):
        try:
            userToken = request.data.get('userToken')
            isSuccess = self.redisService.deleteKey(userToken)

            return Response({'isSuccess': isSuccess}, status=status.HTTP_200_OK)
        except Exception as e:
            print('레디스 토큰 해제 중 에러 발생:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)