import random
from rest_framework import status
from rest_framework.utils import json

from apps.attributes.tests.base_test_case import BaseTestCase
from apps.products.tests.faker.data import FakeProduct
from apps.products.models import Product


# todo[] test create_product permissions
# todo[] Test create a product by the all available inputs (assuming valid data)
# todo[] test create_product if status value is anything other than ('active', 'archived', 'draft')
# todo[] test description field as html DOM in it

# todo[] test create_product with empty options
# todo[] test create_product with invalid option data
# todo[] test create_product 0 or 3 option
# todo[] test create_product max 3 options
# todo[] Test create_product with uniq option-names (valid data)
# todo[] Test create_product with uniq item-names (valid data)
# todo[] Test create_product with duplicate option-names (should be unique for a product)
# todo[] Test create_product with duplicate item-names (should be unique for a product-option)
class ProductCreateViewTest(BaseTestCase):
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

    def test_create_product_with_invalid_payloads(self):
        """
        Test create product with invalid payload scenario
        """

        self.set_admin_authorization()

        # Test with empty payload
        response = self.client.post(self.product_endpoint, data={}, content_type='application/json')
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

    def test_create_product_with_empty_payload(self):
        ...

    def test_create_product_with_blank_fields(self):
        ...

    def test_create_product_with_invalid_payload(self):
        ...

    def test_create_product_without_required_fields(self):
        ...

    def test_create_product_just_required_field(self):
        ...

    def test_create_product_with_duplicate_option_names(self):
        ...

    def test_create_product_with_duplicate_item_names(self):
        ...

    def test_save_with_valid_status(self):
        ...

    def test_save_with_invalid_status(self):
        ...

    def test_retrieve_product_details(self):
        """
        Test retrieve a single product details
        """

        self.set_admin_authorization()

        request = self.client.get(self.product_endpoint)

    def test_create_product_with_options(self):
        """
                Test create a product by the all available inputs (as valid data)
                """

        self.set_admin_authorization()

        payload = json.dumps({
            "product_name": "test product",
            "description": "",
            "status": "active",
            "options": []
        })

        response = self.client.post(self.product_endpoint, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # product_id = response.data['product_id']
        # product = Product.objects.get(pk=product_id)
        # options = Product.objects.retrieve_options(product_id)

        # To see the entire diff and identify the specific differences between the two JSON objects:
        # self.maxDiff = None

        # self.assertEqual(response.json(), {
        #     'product_id': product_id,
        #     'product_name': product.product_name,
        #     'description': product.description,
        #     'status': product.status,
        #     'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        #     'options': options
        # })

    def test_create_product_by_random_options(self):
        """
        Test create product by admin permission
        Test the all input fields name as a jason payload and also in the response body
        """

        self.set_admin_authorization()

        product_name = self.fake_product.generate_name(max_nb_chars=50)
        description = self.fake_product.generate_description(nb_sentences=50)
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
