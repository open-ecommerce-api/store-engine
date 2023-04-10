from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config import settings
from . import serializers


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
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(CreateAPIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # Create the user object
            user = serializer.save()

            # Generate a unique token for the user
            token = Token.objects.get_or_create(user=user)

            # `reverse()` is used to generate the URL for the confirm_signup view
            confirm_url = request.build_absolute_uri(reverse('confirm_signup', args=[str(token[0])]))

            # Send confirmation email
            subject = 'Confirm your email address'
            message = f'Hi {user.email}, please click the link below to confirm your account:\n{confirm_url}'
            from_email = settings.DEFAULT_FROM_EMAIL

            try:
                send_mail(subject, message, from_email, [user.email], fail_silently=False)
            except Exception as e:
                return Response(
                    {'failed': 'Unable to send confirmation email.', 'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
