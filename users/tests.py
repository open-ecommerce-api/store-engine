from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import SignupSerializer


class SigninViewTestCase(APITestCase):
    email = 'test@example.com'
    password = 'testPassword'
    signin_url = '/users/signin/'

    @classmethod
    def setUpTestData(cls):
        # Create a new user with valid credentials.
        cls.user = get_user_model().objects.create_user(
            email=cls.email,
            password=cls.password
        )

    def test_signin_with_valid_credentials(self):
        """
        Try to sign in with the new user's credentials.
        Assert that the response contains the user's token
        """

        data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checks whether the key 'token' exists in the `response.data` dictionary.
        # Indicating that the token value is included in the response data.
        self.assertIn('token', response.data)
        self.assertIsNotNone(response.data['token'])

    def test_signin_with_invalid_credentials(self):
        """
        Try to sign in with an invalid email address or password.
        """

        # Blank email and blank password
        data = {
            'email': '',
            'password': ''
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field may not be blank.'],
            'password': ['This field may not be blank.']
        })

        # invalid email and blank password
        data = {
            'email': 'test',
            'password': ''
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['Enter a valid email address.'],
            'password': ['This field may not be blank.']
        })

        # blank email and invalid password
        data = {
            'email': '',
            'password': 'test'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field may not be blank.'],
        })

        # blank email and invalid password
        data = {
            'email': '',
            'password': 'test'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field may not be blank.'],
        })

        # invalid email and invalid password
        data = {
            'email': 'user',
            'password': 'test'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['Enter a valid email address.'],
        })

        # valid email and password, but user dos not exist
        data = {
            'email': 'user@test.com',
            'password': 'user'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'non_field_errors': ['Unable to log in with provided credentials.'],
        })

    def test_signin_with_missing_fields(self):
        # Test sign-in with missing fields
        data = {
            'email': 'test@a.com'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'password': ['This field is required.']})

        # Empty data
        data = {}
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field is required.'],
            'password': ['This field is required.']
        })

        # Blank email and none password
        data = {
            'email': '',
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field may not be blank.'],
            'password': ['This field is required.']
        })

        # None email and blank password
        data = {
            'password': ''
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field is required.'],
            'password': ['This field may not be blank.']
        })

        # invalid email and none password
        data = {
            'email': 'test',
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['Enter a valid email address.'],
            'password': ['This field is required.']
        })

        # none email and invalid password
        data = {
            'password': 'test'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'email': ['This field is required.'],
        })
