from django.contrib.auth.models import update_last_login
from django.contrib.auth.views import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from . import serializers
from .email import Email


class SignupView(APIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        user.save_totp()
        Email.send_signup_confirmation(user)
        return Response({'detail': 'OTP validation code has been sent to your email'}, status=HTTP_200_OK)


class ConfirmSignupView(APIView):
    serializer_class = serializers.SignupConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        otp = serializer.validated_data['totp']

        if user.is_active:
            return Response({'message': 'Account already activated.'}, status=HTTP_400_BAD_REQUEST)
        if not user.validate_totp(otp):
            return Response({'message': 'Invalid OTP'})

        # Activate the user, email is confirmed
        user.is_active = True
        user.save()

        return Response({'message': 'Account activated successfully.'}, status=HTTP_200_OK)


class SigninView(APIView):
    """
    This code creates a view for user signin.
    When a POST request is sent to this view with the required data, it authenticates the user and logs them in if the
    credentials are valid.
    """
    serializer_class = serializers.SigninSerializer

    def post(self, request):
        """
              When you call `serializer.is_valid()`, the serializer checks whether the data passed into it is valid according
              to the serializer's rules. If the data is valid, the method returns `True`, and you can access the validated
              data using the `serializer.validated_data` attribute. If the data is not valid, the method returns `False`,
              and you can access the errors using the `serializer.errors` attribute. In other words, `serializer.is_valid()`
              checks whether the data being serialized or deserialized is in the correct format and adheres to any validation
              rules specified in the serializer.
      """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token, _ = Token.objects.get_or_create(user=user)

        update_last_login(None, user)

        return Response({'token': token.key}, status=HTTP_200_OK)


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        In the `post` method, we simply delete the token associated with the current user and return a success message.
        If the user was not authenticated, we return an error message with a `400 status code`.
        """
        try:
            Token.objects.filter(user=request.user).delete()
            return Response({"message": "You have been logged out."}, status=HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
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
        Email.send_password_reset(request, user, token)

        return Response({'detail': 'Password reset email sent.'}, status=HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def put(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data, context={'token': token, 'uidb64': uidb64})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password has been reset.'}, status=HTTP_200_OK)


class ChangePasswordView(APIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data)
        user.save()

        Email.send_change_password(user)

        return Response({'detail': 'Password changed successfully'}, status=HTTP_200_OK)


class ChangeEmailView(APIView):
    serializer_class = serializers.ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data

        # save the new email in user session to use after validation
        request.session['email'] = new_email

        user.save_totp()

        Email.send_change_email(user, new_email)

        return Response({'detail': 'An OTP has been sent to your new email'}, status=HTTP_200_OK)


class ChangeEmailConfirmView(APIView):
    serializer_class = serializers.ChangeEmailConfirmSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.validate_totp(serializer.validated_data['totp']):
            return Response({'message': 'Invalid otp.'}, status=HTTP_400_BAD_REQUEST)

        if request.session.get('email'):
            user.email = request.session['email']
            user.save()
            request.session.clear()
            return Response({'message': 'successfully changed your email address'}, status=HTTP_200_OK)
        return Response({'message': 'change email failed'}, status=HTTP_400_BAD_REQUEST)
