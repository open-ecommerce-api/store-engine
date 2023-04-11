from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class SigninSerializer(serializers.Serializer):
    """
    This code creates a serializer for the signin endpoint (sign-in data).
    It also includes a validation method that authenticates the user and raises an error if the credentials are invalid
    or the user is inactive.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        the `validate()` function is a method that you can define in a serializer to provide custom validation logic for
        your data. When you call `is_valid()` on a serializer, it runs the `validate()` method if it exists.

        The `validate()` method is called after all the fields have been deserialized and the default validation has
        been performed. You can use the `validate()` method to perform any additional validation that you need, such as
        checking if two fields are mutually exclusive or if a certain combination of fields is required.
        If the data fails validation, you can raise a `serializers.ValidationError` with an appropriate error message.
        """
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


class SignupSerializer(serializers.Serializer):
    """
    The `SignupSerializer` uses the `EmailField` and `CharField` to validate the email and password fields
    respectively.
    The `create` method is used to create a new user with the validated data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('confirm_password')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):

        try:
            user = get_user_model().objects.create_user(**validated_data)

            # Deactivate the user until the email is confirmed
            user.is_active = False

            user.save()
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({'email': ['This email address is already taken.']})


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
