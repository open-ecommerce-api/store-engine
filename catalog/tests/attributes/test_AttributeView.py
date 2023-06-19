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
        Create users then get token keys.
        Fill a database with sample data.
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

    def test_access_permission(self):
        """
        Test permissions as non-admin user for CRUD methods
        """

        # Check unauthorized access
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            *self.get_crud_methods()
        )

        # Check fake Token key
        self.set_fake_authorization()
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            *self.get_crud_methods()
        )

        # Check permission as a regular user
        self.set_user_authorization()
        self.assert_authorization_HTTP_403_FORBIDDEN(
            *self.get_crud_methods()
        )

    def test_create_attribute(self):
        """
        Create attribute by admin permission
        """

        self.set_admin_authorization()

        response = self.client.post(self.attribute_endpoint, data=self.attribute_new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the attribute field names
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
        Test retrieving a single attribute.
        Test if attribute doesn't exist.
        """

        self.set_admin_authorization()

        response = self.client.get(f"{self.attribute_endpoint}{self.get_attribute_id()}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify the attribute field names
        self.assertEqual(response.data, {
            'id': self.get_attribute_id(),
            'name': self.attribute_saved_name,
        })

        # if attribute doesn't exist
        response = self.client.get(f"{self.attribute_endpoint}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_attribute(self):
        """
        Test updating an attribute.
        Test if attribute doesn't exist.
        """

        self.set_admin_authorization()

        # Test updating an attribute.
        _id = self.get_attribute_id()
        response = self.client.put(f"{self.attribute_endpoint}{_id}/", data={'name': self.attribute_new_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the attribute is updated
        self.assertEqual(response.data, {
            'id': _id,
            'name': self.attribute_new_name,
        })

        # Test if attribute doesn't exist.
        response = self.client.put(f"{self.attribute_endpoint}{999}/", data={'name': self.attribute_new_name})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_attribute(self):
        """
        Test deleting an attribute.
        Test if attribute doesn't exist.
        """

        self.set_admin_authorization()

        delete_url = f"{self.attribute_endpoint}{self.get_attribute_id()}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test if attribute doesn't exist. (Verify the attribute is deleted)
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

    def assert_authorization_HTTP_401_UNAUTHORIZED(self, *methods):
        for method in methods:
            response = method()
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assert_authorization_HTTP_403_FORBIDDEN(self, *methods):
        for method in methods:
            response = method()
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def get_crud_methods(self):
        return (lambda: self.client.get(self.attribute_endpoint),
                lambda: self.client.post(self.attribute_endpoint, data=self.attribute_new_data),
                lambda: self.client.put(f"{self.attribute_endpoint}{self.get_attribute_id()}/",
                                        data=self.attribute_new_data),
                lambda: self.client.delete(f"{self.attribute_endpoint}{self.get_attribute_id()}/"))

    @classmethod
    def create_attributes(cls):
        """
        Helper method to create attributes
        """

        for name in cls.attribute_names:
            Attribute.objects.create(name=name)

    def get_attribute_name(self):
        return self.attribute_saved_name

    def get_attribute_id(self):
        try:
            attribute = Attribute.objects.get(name=self.attribute_saved_name)
            return attribute.id
        except Attribute.DoesNotExist:
            return None
