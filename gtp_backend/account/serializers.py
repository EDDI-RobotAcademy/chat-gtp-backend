from rest_framework import serializers

from account.entity.account import Account

class AccountSerializer(serializers.ModelSerializer):
    loginType = serializers.CharField(source='loginType.loginType', read_only=True)

    class Meta:
        model = Account
        fields = ['id','loginType']