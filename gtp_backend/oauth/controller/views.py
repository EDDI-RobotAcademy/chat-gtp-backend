import uuid

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from oauth.serializer.kakao_oauth_access_token_serializer import KakaoOauthAccessTokenSerializer
from oauth.serializer.kakao_oauth_url_serializer import KakaoOauthUrlSerializer
from oauth.service.oauth_service_impl import OauthServiceImpl
from oauth.service.redis_service_impl import RedisServiceImpl


class OauthView(viewsets.ViewSet):
    oauthService = OauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()


    def kakaoOauthURI(self, request):
        url = self.oauthService.kakaoLoginAddress()
        print(f"url:", url)
        serializer = KakaoOauthUrlSerializer(data={ 'url': url })
        serializer.is_valid(raise_exception=True)
        print(f"validated_data: {serializer.validated_data}")
        return Response(serializer.validated_data)

