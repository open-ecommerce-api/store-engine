from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase


class AttributeViewTestCase(APITestCase):
    attribute_url = "/catalog/attributes/"
    attribute_values_url = "/catalog/attribute-values/"

    @classmethod
    def setUpTestData(cls):
        """
        create a user with admin permission, then get an admin token key
        """

        token, created = Token.objects.get_or_create(
            user=get_user_model().objects.create_superuser('admin@example.com', 'password'))
        cls.admin_token_key = token.key

    def test_create_attribute_unauthorized(self):
        """
        When a user doesn't have an admin permission
        """

        attribute_data = {
            'name': 'Color',
        }
        response = self.client.post(self.attribute_url, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_create_attribute(self):
        """
        Create attribute by admin permission
        """

        # Set Authorization header with token
        self.set_authorization_header()

        # Post new attribute
        attribute_data = {
            'name': 'Color',
        }
        response = self.client.post(self.attribute_url, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': response.data['id'],
            'name': 'Color',
        })

        # test attribute unique name
        response = self.client.post(self.attribute_url, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"name": ["attribute with this name already exists."]})

    # def test_get_attributes(self):
    #     """
    #     Retrieve a list
    #     """

    def set_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token_key}')
