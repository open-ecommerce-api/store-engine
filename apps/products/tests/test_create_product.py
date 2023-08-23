from rest_framework import status
from rest_framework.utils import json
import pprint
from apps.attributes.tests.base_test_case import BaseTestCase
from apps.products.models import Product
from apps.products.tests.faker.data import FakeProduct


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
        # todo[] test create_product permissions
        """
        Test permissions as non-admin user for CRUD methods
        """

    def test_create_simple_product(self):
        """
        TODO Test create a product by the all available inputs (assuming valid data)
        TODO Test response data when I create simple product
        TODO why response.data items is not in the same order as what I wrote in the view and model code?
        """
        self.set_admin_authorization()
        self.maxDiff = None
        payload = {
            "product_name": "Test Product",
            "description": "test description",
            "status": "active",
            "options": [
                {
                    'option_name': 'color',
                    'items': ['red', 'green']
                },
                {
                    'option_name': 'material',
                    'items': ['Cotton', 'Nylon']
                },
                {
                    'option_name': 'size',
                    'items': ['M', 'S']
                }
            ]
        }
        expected_data = {
            'description': 'test description',
            'options': [
                {
                    'items': [
                        {
                            'item_id': 1,
                            'item_name': 'green'},
                        {
                            'item_id': 2,
                            'item_name': 'red'
                        }
                    ],
                    'option_name': 'color',
                    'options_id': 1
                },
                {
                    'items': [
                        {
                            'item_id': 3,
                            'item_name': 'Cotton'
                        },
                        {
                            'item_id': 4,
                            'item_name': 'Nylon'
                        }
                    ],
                    'option_name': 'material',
                    'options_id': 2
                },
                {'items': [{'item_id': 5, 'item_name': 'M'},
                           {'item_id': 6, 'item_name': 'S'}],
                 'option_name': 'size',
                 'options_id': 3}],
            'product_id': 1,
            'product_name': 'Test Product',
            'status': 'active',
            'variants': []}
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assert_datetime_format(response.data.pop('created_at'))
        self.assertEqual(response.data, expected_data)

    def test_create_variable_product(self):
        # TODO Test response data when I create variant product
        ...

    def test_invalid_with_empty_payload(self):
        """
        Test create product with empty payload
        """

        self.set_admin_authorization()
        payload = {}
        expected_data = {
            "product_name": ["This field is required."]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_invalid_without_required_fields(self):
        """
        Test create product without required fields
        """

        self.set_admin_authorization()
        payload = {
            "description": "test description",
        }
        expected_data = {
            "product_name": ["This field is required."]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_invalid_with_blank_required_field(self):
        """
        Test if required fields are blank
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "",
        }
        expected_data = {"product_name": ["This field may not be blank."]}
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_with_all_blank_fields(self):
        """
        Test if all fields are blank
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "",
            "description": "",
            "status": "",
            "options": []
        }
        expected_data = {"product_name": ["This field may not be blank."]}
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_with_invalid_field_name(self):
        """
        Test with invalid field name
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "test product",
            "description_": "",
            "status_": "",
            "options_": []
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_invalid_status(self):
        """
        Test create a product if status value is anything other than ('active', 'archived', 'draft')
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "test product",
            "status": "invalid"
        }
        expected_data = "draft"
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], expected_data)

        payload = {
            "product_name": "test product",
            "status": "invalid_invalid"
        }
        expected_data = {
            "status": ["Ensure this field has no more than 10 characters."]
        }
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_with_uniq_options(self):
        """
        Test create product with uniq option-names (valid data)
        Test create product with uniq item-names (valid data)
        """

        self.set_admin_authorization()
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
        expected_data = {"options": ["A product can have a maximum of 3 options."]}
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_with_invalid_options(self):
        """
        Test create a product with invalid options scenarios
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
        expected_data = None
        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['options'], expected_data)

    def test_with_duplicate_options(self):
        """
        Test create product with duplicate option-names (should be unique for a product)
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

    def test_with_html_description(self):
        # todo[] test description field as html DOM in it
        # unsafe_html = '<script>alert("XSS Attack!");</script>'
        ...

    def test_crete_default_variant(self):
        """
        Test create variant if I want to create a simple product (default variant)
        Test each product should have at least one variant when it was created, even the options is empty
        """

        self.set_admin_authorization()
        payload = {
            "product_name": "test product",
        }
        expected_data = {
            "price": {
                "amount": "0.00",
                "currency": "USD"
            },
            "stock": 0,
            "option1": None,
            "option2": None,
            "option3": None
        }

        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['variants']), 1)
        variants = response.data['variants'][0]
        self.assertEqual(variants['price'], expected_data['price'])
        self.assertEqual(variants['stock'], expected_data['stock'])
        self.assertEqual(variants['option1'], expected_data['option1'])
        self.assertEqual(variants['option2'], expected_data['option2'])
        self.assertEqual(variants['option3'], expected_data['option3'])
        self.assert_datetime_format(variants['created_at'])

        # test with empty list in options
        payload = {
            "product_name": "test product",
            "options": []
        }

        response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['variants']), 1)
        variants = response.data['variants'][0]
        self.assertEqual(variants['price'], expected_data['price'])
        self.assertEqual(variants['stock'], expected_data['stock'])
        self.assertEqual(variants['option1'], expected_data['option1'])
        self.assertEqual(variants['option2'], expected_data['option2'])
        self.assertEqual(variants['option3'], expected_data['option3'])

    def atest_create_variants(self):
        """
        Testr create variant if I want to create a variable product
        """
        # self.set_admin_authorization()
        #
        # payload = {
        #     "product_name": "test product",
        #     "options": [
        #         {
        #             'option_name': 'color',
        #             'items': ['red'],
        #         },
        #         {
        #             'option_name': 'size',
        #             'items': ['M'],
        #         }
        #     ]
        # }
        #
        # response = self.client.post(self.product_endpoint, data=json.dumps(payload), content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #
        # product_id = response.data['product_id']
        # product = Product.objects.get(pk=product_id)
        # variants = Product.objects.retrieve_variants(product_id)
        #
        # self.assertEqual(response.data['variants'], {
        #     {
        #         "id": product.variants[0].id,
        #         "product_id": product_id,
        #         "price": None,
        #         "stock": None,
        #         "option1": "red",
        #         "option2": "M",
        #         "option3": None,
        #     }
        # })
