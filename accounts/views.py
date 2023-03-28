from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import *
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes





class OTPLoginView(APIView):
    def get(self, request):
        serializer = serializers.RequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(data=serializers.RequestOTPResponseSerilizer(otp).data)
            except Exception as e:
                raise
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request):
        serializer = serializers.VerifyOtpRequestSerilzer(data=request.data) 
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['phone'], data['code']):
                return Response(self._handel_login(data))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=serializer.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handel_login(self, otp):
        User = get_user_model()
        query = User.objects.filter(phone=otp['phone'])
        if query.exists():
            created = False
            user = query.first()
        token =Token.objects.get(user=user)
        return serializers.TokenSerilizer({
            'token': str(token),
            'created': created
        }).data


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout_user(request):

    request.user.auth_token.delete()

    # logout(request)
    return Response('logout')