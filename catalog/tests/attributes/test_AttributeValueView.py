from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Attribute
from catalog.tests.attributes.test_AttributeView import AttributeViewTest


class AttributeValueView_Test(AttributeViewTest):
    """
    todo list:
    [] test admin permissions for CRUD (one by admin token, one by user token and one by unauthorized user)
        1. check permission inside the helper class // or check in before create attribute
    [] test validations in CRUD
    [] test create a value(s)
    [] test retrieve a value
    [] test list values
    [] test update a value
    [] test delete a value
    [] test delete multi values
    """
    attribute_values_endpoint = "/catalog/attribute-values/"

    def test_user_permission(self):
        # self.create_value('Color')
        response, attribute_id = self.create_attribute('color')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_values(self):
        """
        Create a new value(s)
        """

        # init
        self.set_admin_authorization()
        self.create_multi_values('Color')

        # blank values
        # blank attribute_id
        ## _missing_fields
        #

    # def test_retrieve_attribute_values(self):
    #     """
    #     Retrieve all values of an attribute
    #     """
    #
    #     # init
    #     self.set_authorization_header()
    #     attribute_values_data, attribute_id = self.create_multi_values('Color')
    #
    #     # Get attribute values
    #     get_url = f"{self.attribute_endpoint}{attribute_id}/values/"
    #     response = self.client.get(get_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, attribute_values_data)

    # def test_list_values(self):
    #     """
    #     Retrieve all values in any attribute.
    #     """
    #
    #     # init
    #     self.set_authorization_header()
    #     self.create_multi_values('Color')
    #     self.create_multi_values('Size')
    #
    #     # retrieve value list
    #     response = self.client.get(self.attribute_values_endpoint)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     attribute_values_data = response.json()
    #
    #     # assert that the response body is a list of dictionaries
    #     self.assertIsInstance(attribute_values_data, list)
    #     for value in attribute_values_data:
    #         self.assertIsInstance(value, dict)
    #         self.assertIn('id', value)
    #         self.assertIn('value', value)
    #         self.assertIn('attribute_id', value)

    # def test_retrieve_value(self):
    #     """
    #     Retrieve a value from an attribute
    #     """
    #
    #     # init
    #     self.set_authorization_header()
    #     value = self.create_value('Color')
    #
    #     # retrieve with valid data
    #     response = self.client.get(f"{self.attribute_values_endpoint}{value['id']}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {
    #         "id": value['id'],
    #         "value": value['value'],
    #         "attribute_id": value['attribute_id']
    #     })
    #
    #     # invalid value ID
    #     response = self.client.get(f"{self.attribute_values_endpoint}11/")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data, {"detail": "Not found."})

    # def test_update_value(self):
    #     """
    #     Update a value.
    #     """
    #
    #     # init
    #     self.set_authorization_header()
    #     value_list, attribute_id = self.create_multi_values('Color')

    # def test_delete_value(self):
    #     ...

    # def test_delete_multi_values(self):
    #     """
    #     Delete multi Values form an attribute.
    #     """

    # def test_unique_value_name(self):
    #     ...

    def create_multi_values(self, attribute_name):
        """
        Helper, Create multi values for an attribute
        """

        # init
        self.set_admin_authorization()
        _, attribute_id = self.create_attribute(attribute_name)

        # Create attribute values
        attribute_values_data = {
            "values": [
                "Red", "Blue", "Green"
            ],
            "attribute_id": attribute_id,
        }
        response = self.client.post(self.attribute_values_endpoint, data=attribute_values_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attribute_values_data = [
            {"id": data['id'], "value": data['value'], "attribute_id": attribute_id} for data in response.data]
        self.assertEqual(response.json(), attribute_values_data)
        return attribute_values_data, attribute_id

        #
        # # Test retrieving attribute values with an invalid attribute ID.
        # invalid_id = "invalid"
        # get_url = f"{self.attribute_url}{invalid_id}/values/"
        # response = self.client.get(get_url)
        #
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(
        #     response.data,
        #     {'detail': 'attributes ID should be integer'}
        # )

    def create_value(self, attribute_name):
        """
        Helper, Create a value
        """

        # init
        self.set_admin_authorization()
        response, attribute_id = self.create_attribute(attribute_name)

        # Create attribute values
        value_data = {
            "values": "Red",
            "attribute_id": attribute_id,
        }
        response = self.client.post(self.attribute_values_endpoint, data=value_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.["id"], response.data["id"])
        # self.assertEqual(response.json()["value"], response.data["value"])
        # self.assertDictEqual(response.json(), {
        #     'id': attribute_id,
        #     'values': 'Color',
        # })
        return value_data
