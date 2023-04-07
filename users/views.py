from django.shortcuts import render
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

from . import serializers

User = get_user_model()


class RegisterView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = Token.objects.create(user=user)
       
        current_site = get_current_site(request).domain
        reletivelink = reverse('verify_email')
        absurl = 'http://'+current_site +reletivelink+"?token="+str(token)
        email_body = 'Hi '+user.email + ' please use linke below to verify your email\n'+ absurl


        data = {'email_body': email_body,'to_email':user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    """
    An endpoint for  verifies the user's email address
    """
    serializer_class = serializers.EmailVerificationSerializer
    def get(self, request, *args, **kwargs):
        token = request.POST.get('token')
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email': 'Successfully verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Already verified'}, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)




     
class LoginView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user = User.objects.get(email=data['email'])
            if user:
                if user.check_password(password):
                    login(request,user)
                    user.save()
                    token =Token.objects.get(user=user)
                    data = serializer.data
                    data['token'] = token.key
                    return Response(data, status=status.HTTP_200_OK)
                return Response({'detail': 'inter password'})
            return Response({'detail': 'user does not exists'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout_user(request):

    request.user.auth_token.delete()

    # logout(request)
    return Response('logout')





@api_view(["POST"])
def adminLogin(request):
    """
    An endpoint for login admin.
    """

    if(request.method=="POST"):
        email = request.data["email"]
        password = request.data["password"]

        authenticated_user = authenticate(request, email=email, password=password)
        if authenticated_user != None:

            if(authenticated_user.is_authenticated and authenticated_user.is_admin):
                login(request,authenticated_user)
                return Response({"Message":"User is Authenticated. "})   
            else:
                return Response({"message":"User is not authenticated. "})
        else:
            return Response({"Message":"Either User is not registered or password does not match"})





class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',  
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ResetPassword(APIView):
    """
    An endpoint for reset password.
    """
    def post(self,request):
        serializer=serializers.ResetPasswordSerializer(data=request.data)
        datas={}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            datas['data']='successfully registered'
            return Response(datas)
        return Response('failed retry after some time')