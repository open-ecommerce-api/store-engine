from string import digits

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_decode


def generate_otp(length) -> str:
    """
    returns an all-numeric OTP code with custom length
    """
    return get_random_string(length=length, allowed_chars=digits)


def get_user(uidb64):
    """
    Retrieves the user object from a stored pk in urlsafe encoded base64 value
    """
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except (
            TypeError,
            ValueError,
            OverflowError,
            get_user_model().DoesNotExist,
            ValidationError,
    ):
        user = None
    return user
