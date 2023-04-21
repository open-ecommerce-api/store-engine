from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import User


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
            user.save()
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({'email': ['This email address is already taken.']})


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        if get_user_model().objects.filter(email=data.get('email')).exists():
            data['user'] = User.objects.get(email=data.get('email'))
        else:
            raise serializers.ValidationError("This email address is not associated with any user account.")
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        # validate token
        try:
            data['token'] = Token.objects.get(key=self.context['token'])
        except Token.DoesNotExist:
            raise serializers.ValidationError('Invalid password reset.')

        # validate new password
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        token = validated_data['token']
        user = token.user
        user.set_password(validated_data['new_password'])
        user.save()

        # Delete the token after password reset
        token.delete()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['user']

        # check old password
        if not check_password(data.get('old_password'), user.password):
            raise serializers.ValidationError('Invalid password')

        # new password should not be the same as old password
        if check_password(data.get('new_password'), user.password):
            raise serializers.ValidationError('New password must be different from old password')

        # validate new password
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("The new password and confirmation do not match.")

        return data.get('new_password')


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['user']

        # check password
        if not user.check_password(data.get('password')):
            raise serializers.ValidationError('Invalid password')

        # check email uniqueness
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('Email already in use')

        return data.get('email')
