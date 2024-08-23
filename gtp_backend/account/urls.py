from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.views import AccountView

router = DefaultRouter()
router.register(r'account',AccountView,basename='account')

urlpatterns = [
    path('',include(router.urls)),
    path('register',
         AccountView.as_view({'post': 'registerAccount'}),
         name='account-register'),
    path('email-duplication-check',
         AccountView.as_view({'post': 'checkEmailDuplication'}),
         name='account-email-duplication-check'),
    path('nickname-duplication-check',
         AccountView.as_view({'post': 'checkNicknameDuplication'}),
         name='account-nickname-duplication-check'),
    path('account-check',
         AccountView.as_view({'post': 'checkPasswordDuplication'}),
         name='account-password-duplication-check'),
]    path('find-nickname',
    path('find-nickname',
         AccountView.as_view({'post':'findNickname'}),
         name='account-find-nickname'),
    path('modify-nickname',
         AccountView.as_view({'post':'modifyNickname'}),
        name='account-modify-nickname'),
    path('modify-password',
         AccountView.as_view({'post':'modifyPassword'}),
        name='account-modify-password'),
    ]