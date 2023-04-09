from django.contrib.auth import authenticate
from rest_framework import serializers


class SigninSerializer(serializers.Serializer):
    """
    This code creates a serializer for the signin endpoint (sign-in data).
    It also includes a validation method that authenticates the user and raises an error if the credentials are invalid
    or the user is inactive.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User is inactive.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        # if it's ok, return valid data
        return data
