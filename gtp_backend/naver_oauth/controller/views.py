import uuid
from urllib import parse

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from naver_oauth.serializer.naver_oauth_url_serializer import NaverOauthUrlSerializer
from naver_oauth.service.naver_oauth_service_impl import NaverOauthServiceImpl


class NaverOauthView(viewsets.ViewSet):
    naverOauthService = NaverOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()

    def naverOauthURI(self, request):
        url = self.naverOauthService.naverLoginAddress()
        print(f"url:", url)
        serializer = NaverOauthUrlSerializer(data={ 'url': url })
        serializer.is_valid(raise_exception=True)
        print(f"validated_data: {serializer.validated_data}")
        return Response(serializer.validated_data)