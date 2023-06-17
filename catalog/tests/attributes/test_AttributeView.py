from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Attribute


class AttributeViewTest(APITestCase):
    """
    Test access permissions for CRUD methods
    Test CRUD results base on the multi scenario
    """

    # init data
    attribute_endpoint = "/catalog/attributes/"  # better to do reverse('catalog:attribute-list')` but I cant fix it

    attribute_names = ['color', 'size', 'material']

    attribute_saved_name = "color"
    attribute_saved_data = {'name': attribute_saved_name, }

    attribute_new_name = "test name"
    attribute_new_data = {'name': attribute_new_name, }

    @classmethod
    def setUpTestData(cls):
        """
        Create a user with admin permission, then get an admin token key.

        """

        # create an admin
        token, created = Token.objects.get_or_create(
            user=get_user_model().objects.create_superuser('admin@example.com', 'test'))
        cls.admin_token_key = token.key

        # create a user
        token, created = Token.objects.get_or_create(
            user=get_user_model().objects.create_user('user@example.com', 'test'))
        cls.user_token_key = token.key

        # fill database
        cls.create_attributes()

    def test_create_attribute_permission(self):
        """
        Test permissions as non-admin user
        """

        # Check unauthorized access
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            self.client.get(self.attribute_endpoint)
        )

        # Check fake Token key
        self.set_fake_authorization()
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            self.client.post(self.attribute_endpoint, data=self.attribute_new_data)
        )

        # Check permission as a regular user
        self.set_user_authorization()
        self.assert_authorization_HTTP_403_FORBIDDEN(
            self.client.post(self.attribute_endpoint, data=self.attribute_new_data)
        )

    def test_create_attribute(self):
        """
        Create attribute by admin permission
        """

        self.set_admin_authorization()

        response = self.client.post(self.attribute_endpoint, data=self.attribute_new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': response.data['id'],
            'name': self.attribute_new_name,
        })

    def test_create_attribute_unique_name(self):
        """
        Create attribute with the same name (case-sensitive) for test unique-name
        """

        # init
        self.set_admin_authorization()
        response = self.client.post(self.attribute_endpoint, data=self.attribute_saved_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"name": ["attribute with this name already exists."]})

    def test_list_attributes(self):
        """
        Retrieve a list of attributes.
        """

        # init
        self.set_admin_authorization()

        response = self.client.get(self.attribute_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # if no data added should get a blank response
        Attribute.objects.all().delete()
        response = self.client.get(self.attribute_endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # fill database
        self.create_attributes()

    def test_retrieve_attribute(self):
        """
        Retrieving a single attribute.
        """

        # init
        self.set_admin_authorization()
        response, attribute_id = self.create_attribute('Color')

        # Retrieving a single attribute, base on what I created
        response = self.client.get(f"{self.attribute_endpoint}{attribute_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': attribute_id,
            'name': 'Color',
        })

    def test_update_attribute(self):
        """
        Updating an attribute.
        """

        # init
        self.set_admin_authorization()
        response, attribute_id = self.create_attribute('Color')

        # Update the attribute, base on what I created
        update_data = {
            'name': 'New Color',
        }
        update_url = f"{self.attribute_endpoint}{attribute_id}/"
        response = self.client.put(update_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': attribute_id,
            'name': 'New Color',
        })

    def test_delete_attribute(self):
        """
        Deleting an attribute.
        """

        # init
        self.set_admin_authorization()
        response, attribute_id = self.create_attribute('Color')

        # Delete the attribute, base on what I created
        delete_url = f"{self.attribute_endpoint}{attribute_id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the attribute is deleted
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

    def assert_authorization_HTTP_401_UNAUTHORIZED(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assert_authorization_HTTP_403_FORBIDDEN(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_attributes(self):
        """
        Helper method to create attributes
        """

        for name in self.attribute_names:
            Attribute.objects.create(name=name)

    # def test_permission(self):
    #     """
    #     Test that only authenticated users with the `is_staff` permission can access the AttributeView viewset.
    #     """
    #     # Unauthenticated user
    #     url = reverse('attribute-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     # Authenticated user without `is_staff` permission
    #     self.client.login(username='user', password='password')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     # Authenticated user with `is_staff` permission
    #     self.client.login(username='admin', password='password')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     # Test all HTTP methods
    #     for method in ['get', 'post', 'put', 'delete']:
    #         self._check_permission(method)

    # def _check_permission(self, method):
    #     """
    #     Test that only authenticated users with the `is_staff` permission can access the AttributeView viewset using the given HTTP method.
    #     """
    #     attribute = Attribute.objects.create(name='Test Attribute')
    #     url = reverse('attribute-detail', args=[attribute.pk])
    #     data = {'name': 'New Attribute Name'}
    #
    #     # Unauthenticated user
    #     response = getattr(self.client, method)(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     # Authenticated user without `is_staff` permission
    #     self.client.login(username='user', password='password')
    #     response = getattr(self.client, method)(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     # Authenticated user with `is_staff` permission
    #     self.client.login(username='admin', password='password')
    #     response = getattr(self.client, method)(url, data=data)
    #     if method in ['post', 'put']:
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     elif method == 'delete':
    #         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     else:
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
