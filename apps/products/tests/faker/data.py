import random

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

    options = ['color', 'size', 'material', 'Style']
    option_color_items = ['red', 'green', 'black', 'blue', 'yellow']
    option_size_items = ['S', 'M', 'L', 'XL', 'XXL']
    option_material_items = ['Cotton', 'Nylon', 'Plastic', 'Wool', 'Leather']
    option_style_items = ['Casual', 'Formal']

    def __init__(self):
        self.product_name = self.generate_name()
        self.product_description = self.generate_description()
        self.product_options = self.generate_duplicate_options()

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

    def generate_duplicate_options(self):
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

    def generate_uniq_options(self):
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
            }
        ]

    def generate_uniq_small_options(self):
        return [
            {
                "option_name": "color",
                "items": self.option_color_items[:1]
            },
            {
                "option_name": "size",
                "items": self.option_size_items[:1]
            }
        ]

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

    def generate_uniq_options_more_than_tree(self):

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
                "option_name": "style",
                "items": self.option_style_items[:2]
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

    def generate_duplicate_items_in_options(self):
        return [
            {
                "option_name": "color",
                "items": ['red', 'green', 'red', 'blue', 'red', 'blue', 'red']
            },
            {
                "option_name": "size",
                "items": ['S', 'M', 'M', 'XL', 'XL']
            },
            {
                "option_name": "material",
                "items": ['Cotton', 'Nylon']
            }
        ]

    def populate_simple_product(self):
        ...

    def populate_variant_product(self):
        ...
