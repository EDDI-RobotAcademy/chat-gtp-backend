from django.db import models

class AccountLoginType(models.Model):

    class LoginType(models.TextChoices):
        KAKAO = 'KAKAO',"kakao"
        GENERAL = "GENERAL","general"
        NAVER = "NAVER","naver"
        GOOGLE = "GOOGLE",'google'

    loginType = models.CharField(max_length=10,choices=LoginType)

    def __str__(self):
        return self.loginType

    class Meta:
        db_table = "account_login_type"
        app_label = "account"
