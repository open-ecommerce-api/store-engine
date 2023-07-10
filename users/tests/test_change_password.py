from django.contrib.auth.hashers import check_password
from django.core import mail
from django.urls import reverse
from rest_framework import status

from .base import AuthenticationBaseTest


class ChangePasswordTestCases(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing login required endpoints without authentication
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    url = reverse('change_password')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {
            'old_password': cls.user1_credentials['password'],
            'new_password': 'test-pass321',
            'confirm_new_password': 'test-pass321'
        }

    def test_change_password(self):
        """
        Ensure logged-in users can change their password
        """

        self._login_user1()
        response = self.client.post(self.url, self.data, format='json')
        user = self._get_user1()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password changed successfully')
        self.assertTrue(check_password('test-pass321', user.password))
        # email confirm
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients()[0], self.user1_credentials['email'])

    # Change password : missing required fields

    def test_change_password_without_old_password(self):
        self._login_user1()
        self.data['old_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['old_password'])

    def test_change_password_without_new_password(self):
        self._login_user1()
        self.data['new_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['new_password'])

    def test_change_password_without_confirm_new_password(self):
        self._login_user1()
        self.data['confirm_new_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['confirm_new_password'])

    # Change password : Invalid credentials
    def test_change_password_using_weak_new_password(self):
        self._login_user1()
        self.data['new_password'] = self.data['confirm_new_password'] = '12345678'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too common.', response.data['new_password'])

    def test_change_password_confirm_using_short_new_password(self):
        self._login_user1()
        self.data['new_password'] = self.data['confirm_new_password'] = '22a'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.data['new_password'])

    def test_change_password_using_invalid_old_password(self):
        self.data['old_password'] = 'wrong-pass123'
        self._login_user1()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid password', response.data['non_field_errors'])

    def test_change_password_using_the_same_old_password_for_new(self):
        self.data['new_password'] = self.data['confirm_new_password'] = self.user1_credentials['password']
        self._login_user1()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('New password must be different from old password', response.data['non_field_errors'])

    def test_change_password_using_different_confirm_password(self):
        self.data['confirm_new_password'] = 'idk-pass22'
        self._login_user1()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The new password and confirmation do not match.', response.data['non_field_errors'])

    def test_change_password_using_anonymous_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', response.data['detail'])
