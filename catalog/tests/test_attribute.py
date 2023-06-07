from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase


class AttributeViewTest(APITestCase):
    # TODO: It is better to do it like this `url = reverse('catalog:attribute-list')` but I cant fix it.
    attribute_url = "/catalog/attributes/"

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
        response = self.client.post(self.attribute_url, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"name": ["attribute with this name already exists."]})

    def test_list_attributes(self):
        """
        Retrieve a list of attributes.
        """

        # init
        self.set_authorization_header()

        # should get a blank response
        response = self.client.get(self.attribute_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create several attributes for test the response data
        attribute_data = [
            {"name": "color"},
            {"name": "size"},
            {"name": "material"}
        ]
        created_attributes = []
        for data in attribute_data:
            response = self.client.post(self.attribute_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_attributes.append(response.data)

        # now retrieve a list of attributes, base on what I created.
        response = self.client.get(self.attribute_url)
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
        response = self.client.get(f"{self.attribute_url}{attribute_id}/")
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
        update_url = f"{self.attribute_url}{attribute_id}/"
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
        delete_url = f"{self.attribute_url}{attribute_id}/"
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
        response = self.client.post(self.attribute_url, data=attribute_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response, response.data['id']


class AttributeValueViewTest(AttributeViewTest):
    attribute_values_url = "/catalog/attribute-values/"

    def test_create_attribute_values(self):
        """
        Retrieving all attribute values of an attribute.
        """

        # init
        self.set_authorization_header()
        response, attribute_id = self.create_attribute('Color')

        # Create attribute values
        attribute_values_data = {
            "values": [
                "Red", "Blue", "Green"
            ],
            "attribute_id": attribute_id,
        }
        response = self.client.post(self.attribute_values_url, data=attribute_values_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get attribute values
        # get_url = f"{self.attribute_url}{attribute_id}/values/"
        # response = self.client.get(get_url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, attribute_values_data)
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
