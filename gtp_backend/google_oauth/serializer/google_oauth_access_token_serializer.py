from rest_framework import serializers


class GoogleOauthAccessTokenSerializer(serializers.Serializer):
    code = serializers.CharField()