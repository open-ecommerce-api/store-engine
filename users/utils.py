from string import digits

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


def generate_otp(length) -> str:
    """
        Generates a random numeric string of the specified length to be used as a time-based
        one-time password (TOTP) code.

        Args:
            length (int): The length of the generated OTP code.

        Returns:
            str: A random numeric string of the specified length.

        Example:
            >>> code = generate_otp(length=6)
            >>> print(code)
            '123456'
    """
    return get_random_string(length=length, allowed_chars=digits)


def validate_passwords_equality(password1, password2):
    if password1 != password2:
        raise ValidationError("Passwords do not match.")
