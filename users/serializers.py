from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import default_token_generator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from users.models import User
from .utils import get_user


class SignupSerializer(serializers.Serializer):
    """
    The `SignupSerializer` uses the `EmailField` and `CharField` to validate the email and password fields
    The `create` method is used to create a new user with the validated data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('confirm_password')

        if password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):

        try:
            user = get_user_model().objects.create_user(**validated_data)
            return user
        except IntegrityError:
            raise ValidationError({'email': ['This email address is already taken.']})


class SignupConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    totp = serializers.CharField(max_length=6, min_length=6, write_only=True)

    def validate(self, data):
        try:
            data['user'] = get_user_model().objects.get(email=data.pop('email'))
            return data
        except get_user_model().DoesNotExist:
            raise ValidationError({'email': 'invalid email.'})


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

        user = authenticate(username=data.get('email'), password=data.get('password'))
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError('Unable to log in with provided credentials.')
        # if it's ok, return valid data
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            data['user'] = get_user_model().objects.get(email=data.get('email'), is_active=True)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("This email address is not associated with any active user account.")

        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        data['user'] = get_user(self.context['uidb64'])

        # validate token
        if not default_token_generator.check_token(data['user'], self.context['token']):
            raise serializers.ValidationError('Invalid password reset.')

        # validate new password
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        user = validated_data['user']
        user.set_password(validated_data['new_password'])
        user.save()
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


class ChangeEmailConfirmSerializer(serializers.Serializer):
    totp = serializers.CharField(max_length=6, min_length=6, write_only=True)
