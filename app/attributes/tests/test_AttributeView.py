from rest_framework import status
from app.attributes.tests.base_test_case import BaseTestCase
from app.attributes.models import Attribute
from app.attributes.tests.faker.data import FakeAttribute as _Data


class AttributeViewTest(BaseTestCase):
    """
    Test access permissions for CRUD methods
    Test CRUD results base on the multi scenario
    """

    # init data
    attribute_endpoint = "/catalog/attributes/"  # better to do reverse('catalog:attribute-list')` but I cant fix it

    # attribute_saved_name = "color"
    attribute_saved_name = _Data.attribute_saved_name

    @classmethod
    def setUpTestData(cls):
        """
        Create users then get token keys.
        Fill a database with sample data.
        """
        super().setUpTestData()

        # fill database
        _Data().populate_attributes()

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

        response = self.client.post(self.attribute_endpoint, data={'name': 'color2', })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the attribute field names
        self.assertDictEqual(response.json(), {
            'id': response.data['id'],
            'name': 'color2',
        })

    def test_create_attribute_unique_name(self):
        """
        Create attribute with the same name (case-sensitive) for test unique-name
        """

        # init
        self.set_admin_authorization()
        response = self.client.post(self.attribute_endpoint, data={'name': _Data.attribute_saved_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"name": ["attribute with this name already exists."]})

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
            'name': _Data.attribute_saved_name,
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
        response = self.client.put(f"{self.attribute_endpoint}{_id}/", data={'name': 'color3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the attribute is updated
        self.assertEqual(response.data, {
            'id': _id,
            'name': 'color3',
        })

        # Test if attribute doesn't exist.
        response = self.client.put(f"{self.attribute_endpoint}{999}/", data={'name': 'test'})
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

    def get_crud_methods(self):
        return (lambda: self.client.get(self.attribute_endpoint),
                lambda: self.client.post(self.attribute_endpoint),
                lambda: self.client.put(f"{self.attribute_endpoint}{self.get_attribute_id()}/"),
                lambda: self.client.delete(f"{self.attribute_endpoint}{self.get_attribute_id()}/"))

    def get_attribute_id(self):
        try:
            attribute = Attribute.objects.get(name=_Data.attribute_saved_name)
            return attribute.id
        except Attribute.DoesNotExist:
            return None
