from django.core import mail
from django.urls import reverse
from rest_framework import status

from .base import AuthenticationBaseTest


class ChangeEmailTestCasses(AuthenticationBaseTest):
    """
    Test cases for authentication endpoints

    These test cases cover the following scenarios:
        - Testing login required endpoints without authentication
        - Testing the serializer and data validation by a variety of inputs
        - Testing the main functionality
        - Testing the response content

    """

    url = reverse('change_email')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {'email': 'user2@test.com', 'password': cls.user1_credentials['password']}

    def test_change_email(self):
        """
        Ensure logged-in users can change their email
        """
        self._login_user1()
        response = self.client.post(self.url, self.data, format='json')
        user = self.User.objects.get(email='user2@test.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Email changed successfully')
        self.assertEqual(user.email, 'user2@test.com')
        # email confirm
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients()[0], self.data['email'])

    def test_change_password_without_email(self):
        self._login_user1()
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['email'])

    def test_change_password_without_password(self):
        self._login_user1()
        self.data['password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['password'])

    def test_change_email_using_invalid_email_format(self):
        self._login_user1()
        self.data['email'] = 'invalid2email'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data['email'])

    def test_change_email_using_invalid_password(self):
        self._login_user1()
        self.data['password'] = 'wrong-pass123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid password', response.data['non_field_errors'])

    def test_change_email_using_taken_email(self):
        self._login_user1()
        response = self.client.post(self.url, self.user1_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email already in use', response.data['non_field_errors'])

    def test_change_email_using_anonymous_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', response.data['detail'])
