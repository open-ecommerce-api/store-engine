"""
It is considered the best practice to define custom managers in a managers.py file in your app's directory.
By doing so, you can keep your models lean and clean and separate the model logic from manager-level functionality
"""
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    It allows you to customize the way users are managed and authenticated in your application.
    This can be useful if you need to add additional fields or functionality to user accounts,
    such as social authentication or two-factor authentication.

    For example, you might override the create_user method to include additional fields when creating a new user,
    or you might override the authenticate method to add support for a custom authentication backend.

    In summary, the benefit of using a custom UserManager in Django is that it allows you to customize the way user
    accounts are managed and authenticated in your application, giving you greater flexibility and control over your
    user authentication system.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.

        We're subclassing the built-in `BaseUserManager` class and overriding its `create_user` method.
        """
        if not email:
            raise ValueError('Email field must be set')

        # `normalize_email` ensure that the email address is correctly formatted and valid before saved to the database
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        """
        about: `self._db`

        By default, Django will use the default database specified in your` DATABASES` at `settings.py` to save objects.
        However, in some cases, you may need to specify a different database to use for saving an object.
        `self._db` is a reference to the database that the UserManager should use to save the user object.
        It is typically used to support multi-database applications where different models are saved to different 
        databases.
        """
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.

        We're subclassing the built-in `BaseUserManager` class and overriding its `create_superuser` method.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have `is_staff=True`')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have `is_superuser=True`')

        return self.create_user(email, password, **extra_fields)
