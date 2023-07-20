from faker import Faker
from faker.providers import lorem
from apps.products.models import Product


class FakeProduct:
    """
    Populates the database with initial data
    """

    # product_name = fa

    def fill_products(self):
        self.populate_products()

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
