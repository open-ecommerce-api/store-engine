from django.core.management.base import BaseCommand
from app.catalog.models import Attribute, AttributeItem


class Command(BaseCommand):
    """
    usage: python manage.py fill_catalog
    """
    help = 'Populates the database with initial data'

    attribute_color_items = ['red', 'green', 'black', 'blue']
    attribute_size_items = ['S', 'M', 'L', 'XL', 'XXL']
    attribute_material_items = ['Cotton', 'Nylon']

    attributes = {
        'color': attribute_color_items,
        'size': attribute_size_items,
        'material': attribute_material_items
    }

    def handle(self, *args, **options):
        self.populate_attributes()

    def populate_attributes(self):
        for attribute_name, item_list in self.attributes.items():
            attribute = Attribute.objects.create(name=attribute_name)

            # create a list of AttributeItem objects using a list comprehension
            item_objects = [AttributeItem(attribute=attribute, item=item) for item in item_list]

            # insert all the AttributeItem objects into the database in a single query
            AttributeItem.objects.bulk_create(item_objects)

    def create_attribute_items(self):
        for attribute_name, item_list in self.attributes.items():
            attribute = Attribute.objects.create(name=attribute_name)

            # create a list of AttributeItem objects using a list comprehension
            item_objects = [AttributeItem(attribute=attribute, item=item) for item in item_list]

            # insert all the AttributeItem objects into the database in a single query
            AttributeItem.objects.bulk_create(item_objects)
