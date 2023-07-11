from django.contrib.auth.models import update_last_login
from django.contrib.auth.views import default_token_generator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
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

        return Response({'detail': 'OTP validation code has been sent to your email'}, status=HTTP_201_CREATED)


class ConfirmSignupView(APIView):
    serializer_class = serializers.SignupConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Activate the user, email is confirmed
        user.is_active = True
        user.save()

        return Response({'message': 'Account activated successfully.'}, status=HTTP_200_OK)


class SigninView(APIView):
    """
        Signin view to obtain authentication token with correct credentials
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

        user = serializer.validated_data

        # generate reset password token
        token = default_token_generator.make_token(user)

        # Send password reset email
        Email.send_password_reset(request, user, token)

        return Response({'detail': 'Password reset email sent.'}, status=HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def put(self, request, token):
        serializer = self.serializer_class(data=request.data, context={'token': token})
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
        # TODO: find a better way to store the user new_email. this approach is not bad for now.
        request.session['new_email'] = new_email

        user.save_totp()

        Email.send_change_email(user, new_email)

        return Response({'detail': 'An OTP has been sent to your new email'}, status=HTTP_200_OK)


class ChangeEmailConfirmView(APIView):
    serializer_class = serializers.TOTPSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.verify_totp(serializer.validated_data['totp']):
            return Response({'message': 'Invalid TOTP.'}, status=HTTP_400_BAD_REQUEST)

        new_email = request.session.get('new_email')

        if new_email:
            user.email = new_email
            user.save()
            request.session.clear()
            return Response({'message': 'successfully changed your email address'}, status=HTTP_200_OK)
        return Response({'message': 'change email failed'}, status=HTTP_400_BAD_REQUEST)
