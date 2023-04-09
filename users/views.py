from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # this line of code will resolve Token error for superuser:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
