from app.catalog.tests.attributes.test_AttributeView import AttributeViewTest
from rest_framework import status
from app.catalog.models import Attribute, AttributeItem


class AttributeValueViewTest(AttributeViewTest):
    """
    [] Test access permissions for CRUD methods
    [] Test CRUD results base on the multi scenario
    [] Test Retrieve all items of an attribute
    [] Test delete multi items
    """
    attribute_items_endpoint = "/catalog/attribute-items/"

    attribute_color_items = ['red', 'green', 'black']
    attribute_size_items = ['S', 'M', 'L', 'XL']
    attribute_material_items = ['Cotton', 'Nylon']

    attributes = {
        'color': attribute_color_items,
        'size': attribute_size_items,
        'material': attribute_material_items
    }

    attribute_new_items = ['new 1', 'new 2', 'new 3']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # fill database
        cls.create_attribute_items()

    @classmethod
    def create_attribute_items(cls):
        """
        Helper method to create attributes
        """

        for attribute_name, item_list in cls.attributes.items():
            attribute = Attribute.objects.get(name=attribute_name)

            # create a list of AttributeItem objects using a list comprehension
            item_objects = [AttributeItem(attribute=attribute, item=item) for item in item_list]

            # insert all the AttributeItem objects into the database in a single query
            AttributeItem.objects.bulk_create(item_objects)

    def test_retrieve_all_items(self):
        """
        Test retrieve all items in any attribute.
        Test if items don't exist.
        """

        self.set_admin_authorization()

        response = self.client.get(self)

        # for attribute_name, items in attribute_items.items():
        #     attribute = Attribute.objects.get(name=attribute_name)
        #     attribute_item_list = [
        #         AttributeItem(attribute=attribute, item=item_name)
        #         for item_name in items
        #     ]
        #     AttributeItem.objects.bulk_create(attribute_item_list)

        # for name in cls.attribute_names:
        #     attribute = Attribute.objects.get(name=name)
        #     item = AttributeItem.objects.create(attribute=attribute, item=item_name)
