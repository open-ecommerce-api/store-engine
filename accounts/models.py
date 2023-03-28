from django.db import models
import random
import string
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .sms_api import send_otp
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class OtpRequestQueryset(models.QuerySet):
    def is_valid(self, phone, code):
        current_time = timezone.now()
        return self.filter(
            phone=phone,
            code=code,
            create__lt=current_time,
            create__gt=current_time - timedelta(seconds=120),
        ).exists()


class OTPManager(models.Manager):
    def get_queryset(self):
        return OtpRequestQueryset(self.model, self._db)

    def is_valid(self, phone, code):
        return self.get_queryset().is_valid(phone=phone, code=code)

    def generate(self, data):
        otp = self.model(phone=data['phone'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp

def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return ''.join(digits)


class OTPRequest(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=30, null=False)
    code = models.CharField(max_length=30, default=generate_otp)
    create = models.DateTimeField(auto_now_add=True, editable=False)
    objects = OTPManager()

