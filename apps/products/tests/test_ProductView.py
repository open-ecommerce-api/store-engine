import random

from rest_framework import status
from faker import Faker
from faker.providers import lorem
from rest_framework.utils import json

from apps.attributes.tests.base_test_case import BaseTestCase
from apps.products.tests.faker.data import FakeProduct as _Data


class ProductViewTest(BaseTestCase):
    """
    Test access permissions for CRUD methods
    Test CRUD results base on the multi scenario
    """

    # init data
    product_endpoint = "/admin/products/"

    fake = Faker()

    options = ['color', 'size', 'material']

    option_color_items = ['red', 'green', 'black', 'blue', 'yellow']
    option_size_items = ['S', 'M', 'L', 'XL', 'XXL']
    option_material_items = ['Cotton', 'Nylon', 'Plastic', 'Wool', 'Leather']

    @classmethod
    def setUpTestData(cls):
        """
        Create users then get token keys.
        Fill a database with sample data.
        """
        super().setUpTestData()

        # fill database
        cls.fake.add_provider(lorem)

    def test_access_permission(self):
        # todo[] test access permissions
        """
        Test permissions as non-admin user for CRUD methods
        """

    def test_create_product(self):
        """
        Test create product by admin permission
        Test the all input fields name as a jason payload and also in the response body
        """

        self.set_admin_authorization()

        product_name = self.fake.text(max_nb_chars=50)
        description = self.fake.paragraph(nb_sentences=50)
        product_status = "draft"
        options = self.generate_random_options()

        payload = json.dumps({
            "product_name": product_name,
            "description": description,
            "status": product_status,
            "options": options
        })

        response = self.client.post(self.product_endpoint, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify response body
        # self.assertEqual(response.json(), {
        #     "product_name": product_name,
        #     "description": description,
        #     "status": product_status,
        #     "options": options
        # })

    def test_create_product_invalid_payload(self):
        """
        todo[*] test with empty payload
        todo[] test with blank fields
        todo[] test without required fields
        todo[] test if status value is anything other than ('active', 'archived', 'draft')
        todo[] test same 'option names'
        todo[] test same 'item names'
        todo[] test 0 or 3 option
        todo[] test max 3 options
        todo[] test
        """

        self.set_admin_authorization()

        # test with empty payload
        payload = json.dumps({})
        response = self.client.post(self.product_endpoint, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "product_name": ["This field is required."]
        })

        # test with blank fields
        payload = json.dumps({
            "product_name": ""
        })
        response = self.client.post(self.product_endpoint, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "product_name": ["This field may not be blank."]
        })

    def generate_random_options(self):

        selected_options = random.sample(self.options, random.randint(0, 3))

        # Select items based on the selected options
        if len(selected_options) > 0:
            selected_items = []
            for option in selected_options:
                match option:
                    case 'color':
                        option1 = {
                            "option_name": option,
                            "items": random.sample(self.option_color_items, random.randint(1, 5))

                        }
                        selected_items.append(option1)

                    case 'size':
                        option2 = {
                            "option_name": option,
                            "items": random.sample(self.option_size_items, random.randint(1, 5))

                        }
                        selected_items.append(option2)
                    case 'material':
                        option3 = {
                            "option_name": option,
                            "items": random.sample(self.option_material_items, random.randint(1, 5))

                        }
                        selected_items.append(option3)

            return selected_items
        else:
            return []
