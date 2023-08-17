from faker import Faker
from faker.providers import lorem
from apps.products.models import Product


class FakeProduct:
    """
    Populates the database with initial data
    """

    fake = Faker()

    product_name = ''
    product_description = ''
    product_status = ''
    product_options = []

    options = ['color', 'size', 'material']
    option_color_items = ['red', 'green', 'black', 'blue', 'yellow']
    option_size_items = ['S', 'M', 'L', 'XL', 'XXL']
    option_material_items = ['Cotton', 'Nylon', 'Plastic', 'Wool', 'Leather']

    def __init__(self):
        self.product_name = self.generate_name()
        self.product_description = self.generate_description()
        self.product_options = self.generate_options()

    def fill_products(self):
        self.fake.add_provider(lorem)
        self.populate_products()

    def populate_single_product(self):
        return Product.objects.create_product(
            {
                "product_name": self.product_name,
                "description": self.product_description,
                "status": "draft",
                "options": self.product_options
            }
        )

    def generate_inputs_for_single_product(self):
        return {
            "product_name": FakeProduct.product_name,
            "description": FakeProduct.product_description,
            "status": FakeProduct,
            "options": FakeProduct
        }

    def generate_name(self):
        return self.fake.text(max_nb_chars=50)

    def generate_description(self):
        return self.fake.paragraph(nb_sentences=50)

    def generate_status(self):
        return "draft"

    def generate_options(self):
        return [
            {
                "option_name": "color",
                "items": self.option_color_items[:2]
            },
            {
                "option_name": "size",
                "items": self.option_size_items[:2]
            },
            {
                "option_name": "material",
                "items": self.option_material_items[:2]
            },
            {
                "option_name": "color",
                "items": self.option_color_items[:3]
            }
        ]

    def populate_products(self):
        fake = Faker()
        fake.name()

        Product.objects.create_product(
            name=fake.text(max_nb_chars=50),
            description=fake.paragraph(nb_sentences=50),
            options=''
        )

    def populate_simple_product(self):
        ...

    def populate_variant_product(self):
        ...
