from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

"""
scenario to do
1. user try to authorize with wrong token key 
"""


class AttributeViewTest(APITestCase):
    # TODO: It is better to do it like this `url = reverse('catalog:attribute-list')` but I cant fix it.
    attribute_endpoint = "/catalog/attributes/"

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
        response = self.client.post(self.attribute_endpoint, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_create_attribute(self):
        """
        Create attribute by admin permission
        """

        # init
        self.set_authorization_header()
        response, attribute_id = self.create_attribute('Color')
        self.assertDictEqual(response.json(), {
            'id': attribute_id,
            'name': 'Color',
        })

    def test_create_attribute_unique_name(self):
        """
        Create attribute with the same name (case-sensitive) for test unique-name
        """

        # init
        self.set_authorization_header()
        self.create_attribute('Color')

        # test attribute unique name
        attribute_data = {
            'name': 'Color',
        }
        response = self.client.post(self.attribute_endpoint, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"name": ["attribute with this name already exists."]})

    def test_list_attributes(self):
        """
        Retrieve a list of attributes.
        """

        # init
        self.set_authorization_header()

        # should get a blank response
        response = self.client.get(self.attribute_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create several attributes for test the response data
        attribute_data = [
            {"name": "color"},
            {"name": "size"},
            {"name": "material"}
        ]
        created_attributes = []
        for data in attribute_data:
            response = self.client.post(self.attribute_endpoint, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_attributes.append(response.data)

        # now retrieve a list of attributes, base on what I created.
        response = self.client.get(self.attribute_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, created_attributes)

    def test_retrieve_attribute(self):
        """
        Retrieving a single attribute.
        """

        # init
        self.set_authorization_header()
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
        self.set_authorization_header()
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
        self.set_authorization_header()
        response, attribute_id = self.create_attribute('Color')

        # Delete the attribute, base on what I created
        delete_url = f"{self.attribute_endpoint}{attribute_id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the attribute is deleted
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def set_authorization_header(self):
        """
        Set the Authorization header with an admin token key.

        In general, `force_authenticate` is a more convenient way to authenticate requests when you are testing your API.
        This is because you don't need to worry about generating and managing tokens.
        However, `self.client.credentials` can be useful if you want to test how your API handles requests that are
        authenticated with tokens.
        """

        # Authentication type: Token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token_key}')

        # Authentication type: Username and password
        # force_authenticate(request, user=self.user)

    def create_attribute(self, name):
        """
        Helper method to create an attribute
        """
        attribute_data = {
            'name': name,
        }
        response = self.client.post(self.attribute_endpoint, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response, response.data['id']

# class AttributeValueViewTest(AttributeViewTest):
#     attribute_values_endpoint = "/catalog/attribute-values/"
#
#     def test_create_values(self):
#         """
#         Create a new value(s)
#         """
#
#         # init
#         self.set_authorization_header()
#         self.create_multi_values('Color')
#
#         # blank values
#         # blank attribute_id
#         ## _missing_fields
#         #
#
#     def test_retrieve_attribute_values(self):
#         """
#         Retrieve all values of an attribute
#         """
#
#         # init
#         self.set_authorization_header()
#         attribute_values_data, attribute_id = self.create_multi_values('Color')
#
#         # Get attribute values
#         get_url = f"{self.attribute_endpoint}{attribute_id}/values/"
#         response = self.client.get(get_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, attribute_values_data)
#
#     def test_list_values(self):
#         """
#         Retrieve all values in any attribute.
#         """
#
#         # init
#         self.set_authorization_header()
#         self.create_multi_values('Color')
#         self.create_multi_values('Size')
#
#         # retrieve value list
#         response = self.client.get(self.attribute_values_endpoint)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         attribute_values_data = response.json()
#
#         # assert that the response body is a list of dictionaries
#         self.assertIsInstance(attribute_values_data, list)
#         for value in attribute_values_data:
#             self.assertIsInstance(value, dict)
#             self.assertIn('id', value)
#             self.assertIn('value', value)
#             self.assertIn('attribute_id', value)
#
#     def test_retrieve_value(self):
#         """
#         Retrieve a value
#         """
#
#         # init
#         self.set_authorization_header()
#         value = self.create_value('Color')
#
#         # retrieve with valid data
#         response = self.client.get(f"{self.attribute_values_endpoint}{value['id']}/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {
#             "id": value['id'],
#             "value": value['value'],
#             "attribute_id": value['attribute_id']
#         })
#
#         # invalid value ID
#         response = self.client.get(f"{self.attribute_values_endpoint}11/")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data, {"detail": "Not found."})
#
#     def test_update_value(self):
#         """
#         Update a value.
#         """
#
#         # init
#         self.set_authorization_header()
#         value_list, attribute_id = self.create_multi_values('Color')
#
#     def test_delete_value(self):
#         ...
#
#     def test_delete_multi_values(self):
#         """
#         Delete multi Values form an attribute.
#         """
#
#     def test_unique_value_name(self):
#         ...
#
#     def create_multi_values(self, attribute_name):
#         """
#         Helper, Create multi values
#         """
#
#         # init
#         self.set_authorization_header()
#         response, attribute_id = self.create_attribute(attribute_name)
#
#         # Create attribute values
#         attribute_values_data = {
#             "values": [
#                 "Red", "Blue", "Green"
#             ],
#             "attribute_id": attribute_id,
#         }
#         response = self.client.post(self.attribute_values_endpoint, data=attribute_values_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         attribute_values_data = [
#             {"id": data['id'], "value": data['value'], "attribute_id": attribute_id} for data in response.data]
#         self.assertEqual(response.json(), attribute_values_data)
#         return attribute_values_data, attribute_id
#
#         #
#         # # Test retrieving attribute values with an invalid attribute ID.
#         # invalid_id = "invalid"
#         # get_url = f"{self.attribute_url}{invalid_id}/values/"
#         # response = self.client.get(get_url)
#         #
#         # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertEqual(
#         #     response.data,
#         #     {'detail': 'attributes ID should be integer'}
#         # )
#
#     def create_value(self, attribute_name):
#         """
#         Helper, Create a value
#         """
#
#         # init
#         self.set_authorization_header()
#         response, attribute_id = self.create_attribute(attribute_name)
#
#         # Create attribute values
#         value_data = {
#             "values": "Red",
#             "attribute_id": attribute_id,
#         }
#         response = self.client.post(self.attribute_values_endpoint, data=value_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # self.assertEqual(response.["id"], response.data["id"])
#         # self.assertEqual(response.json()["value"], response.data["value"])
#         # self.assertDictEqual(response.json(), {
#         #     'id': attribute_id,
#         #     'values': 'Color',
#         # })
#         return value_data
