from rest_framework import status
from rest_framework.utils import json

from apps.attributes.tests.base_test_case import BaseTestCase
from apps.products.tests.faker.data import FakeProduct


# todo[] test create_product permissions
# todo[] Test create a product by the all available inputs (assuming valid data)
# todo[] test description field as html DOM in it


class CreateViewTest(BaseTestCase):
    """
    Test create-product on the multi scenario
    """

    # init data
    product_endpoint = "/admin/products/"

    @classmethod
    def setUpTestData(cls):
        """
        Create users then get token keys.
        Fill a database with sample data.
        """
        super().setUpTestData()

        # fill database
        cls.fake_product = FakeProduct()
        # FakeProduct().populate_single_product()

    def test_access_permission(self):
        # todo[] test access permissions
        """
        Test permissions as non-admin user for CRUD methods
        """

    def test_create_product(self):
        """
        Test create a product by the all available inputs (assuming valid data)
        """

        self.set_admin_authorization()

        payload = {
            "product_name": "test product",
            "description": "test description",
            "status": "active",
            "options": []
        }

        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # product_id = response.data['product_id']
        # product = Product.objects.get(pk=product_id)
        # options = Product.objects.retrieve_options(product_id)
        # self.assertEqual(response.json(), {
        #     'product_id': product_id,
        #     'product_name': product.product_name,
        #     'description': product.description,
        #     'status': product.status,
        #     'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        #     'options': options
        # })

    def test_with_invalid_payloads(self):
        """
        Test create product with invalid payload scenario
        """

        self.set_admin_authorization()

        # Test with empty payload
        response = self.client.post(self.product_endpoint, data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"product_name": ["This field is required."]})

        # Test without required fields
        payload = {
            "description": "test description",
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"product_name": ["This field is required."]})

        # Test if required fields are blank
        payload = {
            "product_name": "",
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"product_name": ["This field may not be blank."]})

        # test if all fields are blank
        payload = {
            "product_name": "",
            "description": "",
            "status": "",
            "options": []
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"product_name": ["This field may not be blank."]})

        # test with invalid field name
        payload = {
            "product_name": "test product",
            "description_": "",
            "status_": "",
            "options_": []
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "product_id": response.data["product_id"],
            "product_name": "test product",
            "description": "",
            "status": "draft",
            "created_at": response.data["created_at"],
            "options": None
        })

    def test_with_invalid_status(self):
        """
        Test create a product if status value is anything other than ('active', 'archived', 'draft')
        """

        self.set_admin_authorization()

        payload = {
            "product_name": "test product",
            "status": "invalid"
        }

        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "draft")

        payload = {
            "product_name": "test product",
            "status": "invalid_invalid"
        }

        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"status": ["Ensure this field has no more than 10 characters."]})

    def test_with_uniq_options(self):
        """
        Test create product with uniq option-names (valid data)
        Test create product with uniq item-names (valid data)
        """

        self.set_admin_authorization()

        # test with 0 or 3 option
        payload = {
            "product_name": "test product",
            "options": self.fake_product.generate_uniq_options()
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_max3_options(self):
        """
        Test create a product by more than three options
        """

        self.set_admin_authorization()

        payload = {
            "product_name": "test product",
            "options": self.fake_product.generate_uniq_options_more_than_tree()
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"options": ["A product can have a maximum of 3 options."]})

    def test_with_invalid_options(self):
        """
        Test create a product with invalid options scenario
        """

        self.set_admin_authorization()

        payload = {
            "product_name": "test product",
            "options": ""
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "option_name": [],
                    "items": ["a", "a", "b", "c", "d", "c", "b", "a"]
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "option_name": "test",
                    "items": ""
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "option_name": "test",
                    "items": [["a", "b"]]
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [{}]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "option_name": "test",
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "items": "test",
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "items": ["a"],
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "product_name": "test product",
            "options": [
                {
                    "x": "test",
                    "y": ["a", "b"]
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_blank_option(self):
        """
        Test create a product with blank option
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "test product",
            "options": []
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['options'], None)

    def test_with_duplicate_options(self):
        """
        Test create_product with duplicate option-names (should be unique for a product)
        """
        self.set_admin_authorization()

        payload = {
            "product_name": self.fake_product.generate_name(),
            "options": [
                {
                    "option_name": "color",
                    "items": ["a"]
                },
                {
                    "option_name": "size",
                    "items": ["a"]
                },
                {
                    "option_name": "material",
                    "items": ["a"]
                },
                {
                    "option_name": "color",
                    "items": ["a"]
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['options']), 3)

    def test_with_duplicate_items_in_options(self):
        """
        Test create product with duplicate item names in options (should be unique for each product-option)
        """
        self.set_admin_authorization()

        payload = {
            "product_name": self.fake_product.generate_name(),
            "options": [
                {
                    "option_name": "color",
                    "items": ['red', 'green', 'red', 'blue', 'red', 'blue', 'red']
                },
                {
                    "option_name": "size",
                    "items": ['S', 'M', 'M']
                },
                {
                    "option_name": "material",
                    "items": ['Cotton', 'Nylon']
                }
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        options = response.data['options']
        self.assertEqual(len(options[0]["items"]), 3)
        self.assertEqual(len(options[1]["items"]), 2)

    def test_remove_empty_options(self):
        """
        Test Remove options if its "items" is empty list
        """

        self.set_admin_authorization()

        payload = {
            "product_name": "string33",
            "options": [
                {
                    "option_name": "color",
                    "items": ["c"]
                },
                {
                    "option_name": "color",
                    "items": ["c"]
                },
                {
                    "option_name": "material",
                    "items": ["m"]
                },
                {
                    "option_name": "size",
                    "items": ["s"]
                },
                {
                    "option_name": "style",
                    "items": []
                },
            ]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['options']), 3)
