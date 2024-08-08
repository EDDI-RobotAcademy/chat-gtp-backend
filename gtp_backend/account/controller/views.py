import hashlib

from rest_framework import viewsets,status
from rest_framework.response import Response
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.serializers import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
load_dotenv()

class AccountView(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()

    def checkEmailDuplication(self, request):
        # url = self.oauthService.kakaoLoginAddress()
        print("checkEmailDuplication()")

        try:
            email = request.data.get('email')
            isDuplicate = self.accountService.checkEmailDuplication(email)
            print(isDuplicate)
            return Response({'isDuplicate': isDuplicate, 'message': 'Email이 이미 존재' \
                             if isDuplicate else 'Email 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self, request):
        # url = self.oauthService.kakaoLoginAddress()
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get('newNickname')
            isDuplicate = self.accountService.checkNicknameDuplication(nickname)

            return Response({'isDuplicate': isDuplicate, 'message': 'nickname이 이미 존재' \
                if isDuplicate else 'nickname 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("nickname 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

