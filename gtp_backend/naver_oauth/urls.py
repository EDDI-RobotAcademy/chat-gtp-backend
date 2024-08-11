from django.urls import path, include
from rest_framework.routers import DefaultRouter

from naver_oauth.controller.views import NaverOauthView

router = DefaultRouter()

router.register(r'naver_oauth', NaverOauthView, basename='naver_oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('naver', NaverOauthView.as_view({'get': 'naverOauthURI'}), name='get-naver-oauth-uri'),
    path('naver/access-token', NaverOauthView.as_view({'post': 'naverAccessTokenURI'}),
                                name='get-naver-access-token-uri'),
    # path('naver/user_info_email',NaverOauthView.as_view({'post':'naverUserEmailURI'}),
    #      name='get-naver-user-info-email-uri'),
    # path('naver/user_info',NaverOauthView.as_view({'post':'naverUserInfoURI'}),
    #      name='get-naver-user-info-uri'),
    # path('redis-access-token/', NaverOauthView.as_view({'post': 'redisGoogleAccessToken'}),
    #                                 name='redis-access-token'),
    # path('logout', NaverOauthView.as_view({'post': 'dropRedisTokenForLogout'}),
    #                             name='drop-redis-token-for-logout')
]