from django.contrib.auth import login
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from . import serializers, email


class SigninView(GenericAPIView):
    """
    This code creates a view for user signin.
    When a POST request is sent to this view with the required data, it authenticates the user and logs them in if the
    credentials are valid.
    """
    serializer_class = serializers.SigninSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Authenticates the user with the provided email and password.
        """

        serializer = self.serializer_class(data=request.data)

        """
        When you call `serializer.is_valid()`, the serializer checks whether the data passed into it is valid according 
        to the serializer's rules. If the data is valid, the method returns `True`, and you can access the validated 
        data using the `serializer.validated_data` attribute. If the data is not valid, the method returns `False`, 
        and you can access the errors using the `serializer.errors` attribute. In other words, `serializer.is_valid()`
        checks whether the data being serialized or deserialized is in the correct format and adheres to any validation
        rules specified in the serializer.
        """
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # this line of code will resolve Token error for superuser:
            token, _ = Token.objects.get_or_create(user=user)

            # update the `last_login` field in the user table
            login(request, user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(CreateAPIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # create a new user and deactivate the user until the email is confirmed
            user = serializer.save(is_active=False)

            # Generate a unique token for the user
            token = Token.objects.get_or_create(user=user)

            # Send confirmation email
            email.SendEmail.send_signup_confirmation(request, user, token)

            return Response(
                {'Confirm email': 'Please check your email to confirm your address'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmSignupView(GenericAPIView):
    def get(self, request, token):
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'Account already activated.'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the user, email is confirmed
        user.is_active = True
        user.save()

        return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    It is recommended to provide a way for users to log out of an application in a REST API.
    Logging out terminates the user's session and invalidates their authentication token. This helps to ensure the
    security of the user's account and data, especially if the user is accessing the application from a public or
    shared device.

    To access a view that requires authentication, you need to include the authentication credentials in the request
    headers.
    One way to do this is to include the token key in the Authorization header of the request.

    For example, to test this endpoint, you should include the token key in the `Authorization` header like this :
    `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`

    (In swagger click on lock icon and add value like this: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, ):
        """
        In the `post` method, we simply delete the token associated with the current user and return a success message.
        If the user was not authenticated, we return an error message with a `400 status code`.
        """
        try:
            token = request.auth
            token.delete()
            return Response({"message": "You have been logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Delete any existing tokens for the user
        Token.objects.filter(user=user).delete()
        # Create a new token for the user
        token = Token.objects.create(user=user)

        # Send password reset email
        email.SendEmail.send_password_reset(request, user, token)

        return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'token': kwargs.get('token')})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)


class ChangePasswordView(GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data)
        user.save()

        # send mail
        email.SendEmail.send_change_password(user)

        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)


class ChangeEmailView(APIView):
    serializer_class = serializers.ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.email = serializer.validated_data
        user.save()

        # send email
        email.SendEmail.send_change_email(user.email)

        return Response({'detail': 'Email changed successfully'}, status=status.HTTP_200_OK)
