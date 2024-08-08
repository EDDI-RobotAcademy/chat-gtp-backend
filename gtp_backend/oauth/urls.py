from django.urls import path, include
from rest_framework.routers import DefaultRouter

from oauth.controller.views import OauthView

router = DefaultRouter()

router.register(r'oauth', OauthView, basename='oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('kakao', OauthView.as_view({'get': 'kakaoOauthURI'}), name='get-kakao-oauth-uri'),
    path('kakao/access-token', OauthView.as_view({'post': 'kakaoAccessTokenURI'}),
                                name='get-kakao-access-token-uri'),
    path('kakao/user-info', OauthView.as_view({'post': 'kakaoUserInfoURI'}),
         name='get-kakao-user-info-uri'),
    path('redis-access-token/', OauthView.as_view({'post': 'redisAccessToken'}),
                                    name='redis-access-token'),
    path('logout', OauthView.as_view({'post': 'dropRedisTokenForLogout'}),
                                name='drop-redis-token-for-logout')
]