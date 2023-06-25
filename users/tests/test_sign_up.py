from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .base import AuthenticationBaseTest


class SignUpTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:

        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    url = reverse('signup')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {'email': 'test@test.com', 'password': 'test-pass123', 'confirm_password': 'test-pass123'}

    def test_signup(self):
        """
        Ensure we can create an inactive user object, a token, and send email
        """

        response = self.client.post(self.url, self.data, format='json')
        created_user = self.User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.User.objects.count(), 2)
        self.assertEqual(created_user.username, 'test@test.com')
        self.assertEqual(created_user.email, 'test@test.com')
        self.assertFalse(created_user.is_active)
        # Token creation
        self.assertEqual(Token.objects.count(), 2)
        self.assertTrue(Token.objects.filter(user=created_user).exists())
        # Verify email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(reverse('confirm_signup', args=[created_user.auth_token.key]), mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].recipients()[0], self.data['email'])

    # Signup : missing required fields
    def test_signup_without_email(self):
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['email'])

    def test_signup_without_password(self):
        self.data['password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['password'])

    def test_signup_without_password_confirm(self):
        self.data['confirm_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['confirm_password'])

    # Signup : invalid credentials

    def test_signup_using_invalid_email_format(self):
        self.data['email'] = 'invalid2email'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data['email'])

    def test_signup_using_weak_password(self):
        self.data['password'] = self.data['confirm_password'] = '12345678'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too common.', response.data['password'])

    def test_signup_using_short_password(self):
        self.data['password'] = self.data['confirm_password'] = '22aa'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.', response.data['password'])

    def test_signup_using_different_password_and_password_confirm(self):
        self.data['confirm_password'] = 'different-pass23'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match.', response.data['non_field_errors'])

    def test_signup_using_taken_email(self):
        self.data['email'] = self.user1_credentials['email']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This email address is already taken.', response.data['email'])


class ConfirmSignUpTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing login required endpoints without authentication
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    def test_confirm_signup(self):
        self._inactive_user1()
        response = self.client.get(reverse('confirm_signup', args=[str(self.user1_token)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self._get_user1().is_active)
        self.assertEqual(response.data['message'], 'Account activated successfully.')

    def test_confirm_signup_using_invalid_token(self):
        self._inactive_user1()
        response = self.client.get(reverse('confirm_signup', args=['invalid-token22ae']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid token.')
        self.assertFalse(self._get_user1().is_active)

    def test_confirm_signup_using_activated_user(self):
        response = self.client.get(reverse('confirm_signup', args=[str(self.user1_token)]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Account already activated.')
