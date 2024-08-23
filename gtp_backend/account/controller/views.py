import hashlib

from dotenv import load_dotenv
from rest_framework import viewsets,status
from rest_framework.response import Response
import os
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

    def checkPasswordDuplication(self, request):
        # url = self.oauthService.kakaoLoginAddress()
        print("checkPasswordDuplication()")

        try:
            email = request.data.get('email')
            password = request.data.get('password')
            hashed = os.getenv('SALT').encode('utf-8') + password.encode("utf-8")
            hash_obj = hashlib.sha256(hashed)
            password = hash_obj.hexdigest()

            isDuplicate = self.accountService.checkPasswordDuplication(email,password)

            return Response({'isDuplicate': isDuplicate, 'message': 'password가 이미 존재' \
                if isDuplicate else 'password 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("password 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def registerAccount(self, request):
        try:
            email = request.data.get('email')
            nickname = request.data.get('nickname')
            password = request.data.get('password')
            logintype = request.data.get('logintype')
            hashed = os.getenv('SALT').encode('utf-8') + password.encode("utf-8")
            hash_obj = hashlib.sha256(hashed)
            password = hash_obj.hexdigest()
            account = self.accountService.registerAccount(
                loginType=logintype,
                email=email,
                nickname=nickname,
                password=password
            )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def findNickname(self,request):
        email = request.data.get('email')
        print(f"email:{email}")
        if not email:
            return Response(None,status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)

        if profile is None:
            return Response(
                {"error":"Profile not found"},status=status.HTTP_400_BAD_REQUEST
            )
        nickname = profile.nickname
        print(f"nickname: {nickname}")
        return Response(nickname,status=status.HTTP_200_OK)

    def modifyNickname(self,request):
        email = request.data.get('email')
        newNickname = request.data.get('newNickname')

        if not email:
            return Response(None,status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)

        if profile is None:
            return Response(
                {"error":"Profile not found"},status=status.HTTP_400_BAD_REQUEST
            )
        profile.nickname = newNickname
        profile.save()
        print(f"nickname: {profile.nickname}")
        return Response(profile.nickname,status=status.HTTP_200_OK)

    def modifyPassword(self,request):
        email = request.data.get('email')
        newPassword = request.data.get('newPassword')
        hashed = os.getenv('SALT').encode('utf-8') + newPassword.encode("utf-8")
        hash_obj = hashlib.sha256(hashed)
        newpassword1 = hash_obj.hexdigest()

        if not email:
            return Response(None,status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)

        if profile is None:
            return Response(
                {"error":"Profile not found"},status=status.HTTP_400_BAD_REQUEST
            )
        profile.password = newpassword1
        profile.save()
        print(f"newPassword: {profile.password}")
        return Response(profile.password,status=status.HTTP_200_OK)