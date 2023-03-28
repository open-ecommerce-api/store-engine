from rest_framework import serializers
from .models import OTPRequest


class RequestOTPResponseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['phone','code']


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=50, allow_null=False)


class RequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=50, allow_null=False)
   

class VerifyOtpRequestSerilzer(serializers.Serializer):
    phone = serializers.CharField(max_length=65, allow_null=False)
    code = serializers.CharField(max_length=4, allow_null=False)


class TokenSerilizer(serializers.Serializer):
    token = serializers.CharField(max_length=120, allow_null=False)
    created = serializers.BooleanField()


