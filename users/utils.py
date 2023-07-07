from string import digits

from django.utils.crypto import get_random_string


def generate_otp(length) -> str:
    """
    returns an all-numeric OTP code with custom length
    """
    return get_random_string(length=length, allowed_chars=digits)
