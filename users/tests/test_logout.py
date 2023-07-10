from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .base import AuthenticationBaseTest


class LogOutTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing login required endpoints without authentication
        - Testing the main functionality
        - Testing the response content

    """
    url = reverse('logout')

    def test_logout(self):
        self._login_user1()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have been logged out.')
        self.assertNotIn(self.user1_token, Token.objects.all())

    def test_logout_using_anonymous_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', response.data['detail'])
