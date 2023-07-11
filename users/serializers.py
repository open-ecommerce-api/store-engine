from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import default_token_generator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from .utils import validate_passwords_equality

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """
        Signup serializer to validate email and password along with its confirmation.
        - create : to create a user with provided credentials.
    """

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # the 'confirm_password' must be omitted from data
        validate_passwords_equality(data['password'], data.pop('confirm_password'))
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise ValidationError({'email': ['This email address is already taken.']})
        return user


class SignupConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    totp = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Serializer validation is used to validate the incoming data before creating or updating an object.
        """
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise ValidationError({'email': 'invalid email.'})

        if user.is_active:
            raise ValidationError({'message': 'Account already activated.'})

        if not user.verify_totp(data['totp']):
            raise ValidationError({'message': 'Invalid TOTP'})

        return user


class SigninSerializer(serializers.Serializer):
    """
        Signin Serializer to validate user credentials and activity.
    """
    email = serializers.EmailField(write_only=True)
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

        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Unable to log in with provided credentials.')
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("This email address is not associated with any active user account.")

        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        try:
            data['user'] = User.objects.get(email=data['email'], is_active=True)
        except User.DoesNotExist:
            raise ValidationError({'email': 'this email is associated with no user'})

        # validate token
        if not default_token_generator.check_token(data['user'], self.context['token']):
            raise serializers.ValidationError('Invalid password reset.')

        # validate new password
        validate_passwords_equality(data['new_password'], data.pop('confirm_new_password'))

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
        if not user.check_password(data['old_password']):
            raise ValidationError('Invalid password')

        validate_passwords_equality(data['new_password'], data.pop('confirm_new_password'))

        return data.get('new_password')


class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['user']

        # check password
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Invalid password')

        # check email uniqueness
        if User.objects.filter(email=data['new_email']).exists():
            raise serializers.ValidationError('Email already in use')

        return data['new_email']


class TOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('totp',)
        extra_kwargs = {'totp': {'write_only': True}}
