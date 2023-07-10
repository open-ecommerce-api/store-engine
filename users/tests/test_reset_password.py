from django.contrib.auth.hashers import check_password
from django.core import mail
from django.urls import reverse
from rest_framework import status

from .base import AuthenticationBaseTest


class ResetPasswordTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing login required endpoints without authentication
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """
    url = reverse('password_reset')

    def test_password_reset(self):
        """
        Ensure the email is sent
        """
        data = {'email': self.user1_credentials['email']}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password reset email sent.')
        # email validation
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients()[0], self.user1_credentials['email'])

    # Password reset : missing required fields
    def test_password_reset_without_email(self):
        data = {'email': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['email'])

    # Password reset : invalid credentials
    def test_password_reset_using_invalid_email_format(self):
        data = {'email': 'invalid22email'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data['email'])

    def test_password_reset_using_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid@inv.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This email address is not associated with any user account.', response.data['non_field_errors'])


class PasswordResetConfirm(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {'new_password': 'new-pass123', 'confirm_new_password': 'new-pass123'}
        cls.url = reverse('password_reset_confirm', args=[str(cls.user1_token)])

    def test_password_reset_confirm(self):
        """
        Ensure password changes
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password has been reset.')
        self.assertTrue(check_password('new-pass123', self._get_user1().password))

    # password Reset confirm : missing required fields

    def test_password_reset_confirm_without_new_password(self):
        self.data['new_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['new_password'])

    def test_password_reset_confirm_without_confirm_new_password(self):
        self.data['confirm_new_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['confirm_new_password'])

    # Password reset confirm : Invalid credentials

    def test_password_reset_confirm_using_weak_new_password(self):
        self.data['new_password'] = self.data['confirm_new_password'] = '12345678'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too common.', response.data['new_password'])

    def test_password_reset_confirm_using_short_new_password(self):
        self.data['new_password'] = self.data['confirm_new_password'] = '22a'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.data['new_password'])

    def test_password_reset_confirm_using_different_password_and_confirm_password(self):
        self.data['confirm_new_password'] = 'different-pass123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match.', response.data['non_field_errors'])

    def test_password_reset_confirm_using_invalid_token(self):
        response = self.client.post(reverse('password_reset_confirm', args=['invalid-token22']), self.data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid password reset.', response.data['non_field_errors'])
