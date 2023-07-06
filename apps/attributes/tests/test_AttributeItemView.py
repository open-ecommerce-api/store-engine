from rest_framework import status
from rest_framework.utils import json

from apps.attributes.tests.faker.data import FakeAttribute as _Data
from apps.attributes.tests.base_test_case import BaseTestCase
from apps.attributes.models import Attribute, AttributeItem


class AttributeItemViewTest(BaseTestCase):
    attribute_items_endpoint = "/admin/attribute-items/"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # populate database
        _Data().populate_attributes_items()

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

    def test_create_item(self):
        """
        Test Create a new item for an attribute.
        """

        self.set_admin_authorization()

        response = self.client.post(self.attribute_items_endpoint, data={'items': ['red2'], 'attribute_id': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify response body
        self.assertEqual(response.json(), [{
            'id': response.data[0]['id'],
            'item': 'red2',
            'attribute_id': 1
        }])

        # Data values are automatically converted to lists, is the default behavior of the Django "test client's post"
        # method when you pass a dictionary as the data parameter.

        # By using json.dumps to serialize the data to a JSON string and passing it as the data parameter,
        # along with specifying the content_type as `application/json`,you can send the payload as a JSON object
        # without the automatic conversion to lists.

        data = json.dumps({'items': 'red2', 'attribute_id': 1})
        response = self.client.post(self.attribute_items_endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_items(self):
        """
        Test Create a new items for an attribute.
        """

        self.set_admin_authorization()

        data = {'items': ['red3', 'red4'], 'attribute_id': 1}
        response = self.client.post(self.attribute_items_endpoint, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify response body
        self.assertEqual(response.json(), [
            {
                'id': response.data[0]['id'],
                'item': 'red3',
                'attribute_id': 1
            },
            {
                'id': response.data[1]['id'],
                'item': 'red4',
                'attribute_id': 1
            }
        ])

    def test_list_items(self):
        """
        Test retrieve all items in any attribute.
        Test if items don't exist.
        """

        self.set_admin_authorization()

        response = self.client.get(self.attribute_items_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_item(self):
        """
        Retrieve a single item.
        """

        self.set_admin_authorization()
        response = self.client.get(f"{self.attribute_items_endpoint}{self.get_item_id()}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify response body
        self.assertEqual(response.data, {
            'id': self.get_item_id(),
            'item': _Data.item_saved_name,
            'attribute_id': 1
        })

        # if attribute doesn't exist
        response = self.client.get(f"{self.attribute_items_endpoint}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """
        Test update a item.
        """

        self.set_admin_authorization()

        _id = self.get_item_id()
        response = self.client.put(f"{self.attribute_items_endpoint}{_id}/", data={"item": "Red112"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify response body
        self.assertEqual(response.data, {
            'id': _id,
            'item': 'Red112',
        })

        # Test if item doesn't exist
        response = self.client.put(f"{self.attribute_items_endpoint}{999}/", data={'item': 'test'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        """
        Test delete a single item
        """

        self.set_admin_authorization()

        delete_url = f"{self.attribute_items_endpoint}{self.get_item_id()}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # verify the item is deleted
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_multi_item(self):
        """
        Delete multi items form an attribute.
        """

        self.set_admin_authorization()

        item_ids = [1, 2, 3]
        response = self.client.post(self.attribute_items_endpoint + 'delete-items/', data={"item_ids": item_ids})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], f'{len(item_ids)} attribute items deleted successfully.')

        response = self.client.post(self.attribute_items_endpoint + 'delete-items/', data={"item_ids": item_ids})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No attribute items found to delete.')

        response = self.client.post(self.attribute_items_endpoint + 'delete-items/', data={"item": item_ids})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"item_ids": ['This field is required.']})

    def test_retrieve_items_by_attribute(self):
        """
        Test retrieve all items of an attribute.
        """

        self.set_admin_authorization()

        response = self.client.get(f"/admin/attributes/{1}/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/admin/attributes/{999}/items/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def get_crud_methods(self):
        return (lambda: self.client.get(self.attribute_items_endpoint),
                lambda: self.client.post(self.attribute_items_endpoint),
                lambda: self.client.put(self.attribute_items_endpoint),
                lambda: self.client.delete(self.attribute_items_endpoint))

    @staticmethod
    def get_item_id():
        try:
            attribute = AttributeItem.objects.get(item=_Data.item_saved_name)
            return attribute.id
        except Attribute.DoesNotExist:
            return None
