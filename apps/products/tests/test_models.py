from django.test import TestCase
from apps.products.models import Product, ProductOption, ProductOptionItem


class ProductQuerySetTestCase(TestCase):

    def setUpTestData(self):
        # Create some initial data for testing
        self.product_data = {
            'product_name': 'Test Product',
            'description': 'This is a test product',
            'status': 'draft',
        }

        self.options_data = [
            {
                'option_name': 'color',
                'items': ['red', 'green', 'blue']
            },
            {
                'option_name': 'size',
                'items': ['S', 'M', 'L']
            }
        ]

    def test_create_product_with_options(self):
        # Test creating a product with options
        product, options = Product.objects.create_product(**self.product_data, options=self.options_data)

    def test_create_product_without_options(self):
        # Test creating a product without options
        product, options = Product.objects.create_product(**self.product_data)

        # Check if the product is created
        self.assertIsNotNone(product.id)

        # Check if the options are None
        self.assertIsNone(options)

        # Check if the product has no options
        self.assertEqual(len(product.productoption_set.all()), 0)


class ProductModelTestCase(TestCase):

    def test_product_status_default_value(self):
        # Test if the product status is set to 'draft' by default
        product = Product.objects.create(product_name='Test Product')
        self.assertEqual(product.status, 'draft')

    def test_product_status_choices(self):
        # Test if the product status only accepts valid choices
        product = Product.objects.create(product_name='Test Product', status='invalid_status')
        with self.assertRaises(ValueError):
            product.full_clean()

    # Add more test cases for other model functions if needed


class ProductOptionModelTestCase(TestCase):
    # Add test cases for the ProductOption model if needed
    pass


class ProductOptionItemModelTestCase(TestCase):
    # Add test cases for the ProductOptionItem model if needed
    pass
