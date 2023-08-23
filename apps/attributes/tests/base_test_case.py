from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create users then get token keys.
        Fill a database with sample data.
        """

        # create an admin
        token, created = Token.objects.get_or_create(
            user=get_user_model().objects.create_superuser('admin@example.com', 'test'))
        cls.admin_token_key = token.key

        # create a user
        token, created = Token.objects.get_or_create(
            user=get_user_model().objects.create_user('user@example.com', 'test'))
        cls.user_token_key = token.key

    def set_admin_authorization(self):
        """
        Set the Authorization Token in header by an admin token key.

        In general, `force_authenticate` is a more convenient way to authenticate requests when you are testing your API.
        This is because you don't need to worry about generating and managing tokens.
        However, `self.client.credentials` can be useful if you want to test how your API handles requests that are
        authenticated with tokens.
        """

        # Authentication type: Token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token_key}')

        # Authentication type: Username and password
        # force_authenticate(request, user=self.user)

    def set_fake_authorization(self):
        """
        Set the Authorization Token in header by a fake token key.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'fake_token_key')

    def set_user_authorization(self):
        """
        Set the Authorization Token in header by a user token key.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token_key}')

    def assert_authorization_HTTP_401_UNAUTHORIZED(self, *methods):
        for method in methods:
            response = method()
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assert_authorization_HTTP_403_FORBIDDEN(self, *methods):
        for method in methods:
            response = method()
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assert_datetime_format(self, date):
        formatted_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(date, formatted_date)
