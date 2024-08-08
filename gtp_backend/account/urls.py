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
    path('password-duplication-check',
         AccountView.as_view({'post': 'checkPasswordDuplication'}),
         name='account-password-duplication-check'),
]