from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthenticationBaseTest(APITestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.user1_credentials = {'email': 'user1@test.com', 'password': 'test-pass123'}
        cls.user1 = cls.User.objects.create_user(**cls.user1_credentials, is_active=True)
        cls.user1_token = Token.objects.create(user=cls.user1)

    def _login_user1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token.key))

    def _get_user1(self):
        return self.User.objects.get(email=self.user1_credentials['email'])

    def _inactive_user1(self):
        self.user1.is_active = False
        self.user1.save()
