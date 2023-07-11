from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from .managers import UserManager
from .utils import generate_otp


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=False, null=False)

    totp = models.CharField(max_length=12, null=True, blank=True)

    totp_valid_until = models.DateTimeField(
        default=now,
        help_text="The timestamp of the moment of expiry of the saved token.",
    )

    USERNAME_FIELD = 'email'

    # fix error [users.User: (auth.E002)], so you should remove 'email' from the 'REQUIRED_FIELDS', like this.
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def save_totp(self, length=6):
        """
        usage: saves a TOTP and expiration time based on settings for user.
        Args:
            length (int): The length of the TOTP code to generate (default: 6).
        """

        self.totp = generate_otp(length)
        self.totp_valid_until = now() + timedelta(seconds=settings.TOTP_EXPIRATION_TIME)
        self.save()

    def verify_totp(self, totp):
        """
            usage: Verifies a token by content and expiry.

            Args:
               totp (str): The TOTP code to validate.
            Returns:
               bool: True if the TOTP is valid and has not expired, False otherwise.
        """
        _now = now()
        if (
                (self.totp is not None)
                and (self.totp == totp)
                and (_now < self.totp_valid_until)
        ):
            self.totp = None
            self.totp_valid_until = _now
            self.save()
            return True
        return False
