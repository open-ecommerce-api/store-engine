from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from .managers import UserManager
from .utils import generate_otp


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)

    totp = models.CharField(max_length=12, null=True)
    totp_valid_until = models.DateTimeField(default=now)

    USERNAME_FIELD = 'email'

    # fix error [users.User: (auth.E002)], so you should remove 'email' from the 'REQUIRED_FIELDS', like this.
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def save_totp(self, length=6):
        """
        saves a (default 6-digit) timed based otp for user
        """
        self.totp = generate_otp(length)
        self.totp_valid_until = now() + timedelta(seconds=settings.OTP_EXPIRATION)
        self.save()

    def validate_totp(self, otp: str) -> bool:
        if (
                (self.totp is not None)
                and (self.totp == otp)
                and (now() < self.totp_valid_until)
        ):
            self.totp = None
            self.totp_valid_until = now()
            return True
        return False
