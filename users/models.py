from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    
    def create_user(self, email, password):
        """
        creates and saves a user with the given email and password
        """
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

        

    def create_superuser(self, email, password):
        """
        creates and saves a superuser with the given email and password
        """
        user = self.create_user( email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField( max_length=128, null=True,blank=True)
    password = models.CharField(max_length=128, null=True,blank=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=30, unique=True, default=uuid.uuid1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


