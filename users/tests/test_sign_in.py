from django.urls import reverse
from rest_framework import status

from .base import AuthenticationBaseTest


class SignInTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    url = reverse('signin')

    def test_signin(self):
        """
        Ensure endpoint returns token
        """
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], str(self.user1_token))

    # signin : missing required fields

    def test_signin_without_email(self):
        self.user1_credentials['email'] = ''
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['email'])

    def test_signin_without_password(self):
        self.user1_credentials['password'] = ''
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['password'])

    # signin : invalid credentials

    def test_signin_using_invalid_email(self):
        self.user1_credentials['email'] = 'invalid@email.com'
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unable to log in with provided credentials.', response.data['non_field_errors'])

    def test_signin_using_invalid_password(self):
        self.user1_credentials['password'] = 'invalid-pass123'
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unable to log in with provided credentials.', response.data['non_field_errors'])

    def test_signin_using_inactive_user(self):
        self._inactive_user1()
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unable to log in with provided credentials.', response.data['non_field_errors'])

    def test_signin_using_invalid_email_format(self):
        self.user1_credentials['email'] = 'invalid2email'
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data['email'])
