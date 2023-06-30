from app.attributes.tests.base import BaseTestCase
from app.attributes.models import Attribute, AttributeItem


class AttributeValueViewTest(BaseTestCase):
    """
    [] Test access permissions for CRUD methods
    [] Test CRUD results base on the multi scenario
    [] Test Retrieve all items of an attribute
    [] Test delete multi items
    """
    attribute_items_endpoint = "/catalog/attribute-items/"

    color_items = ['red', 'green', 'black']
    size_items = ['S', 'M', 'L', 'XL']
    material_items = ['Cotton', 'Nylon']

    item_saved_name = 'red'
    item_saved_data = {'item': item_saved_name}

    attributes = {
        'color': color_items,
        'size': size_items,
        'material': material_items
    }

    new_items = ['new 1', 'new 2', 'new 3']

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

        # for attribute_name, item_list in cls.attributes.items():
        #     attribute = Attribute.objects.get(name=attribute_name)

        # create a list of AttributeItem objects using a list comprehension
        # item_objects = [AttributeItem(attribute=attribute, item=item) for item in item_list]

        # insert all the AttributeItem objects into the database in a single query
        # AttributeItem.objects.bulk_create(item_objects)

    def test_access_permission(self):
        """
        Test permissions as non-admin user for CRUD methods
        """

        # Check unauthorized access
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            *self.get_crud_methods()
        )

        # Check fake Token key
        self.set_fake_authorization()
        self.assert_authorization_HTTP_401_UNAUTHORIZED(
            *self.get_crud_methods()
        )

        # Check permission as a regular user
        self.set_user_authorization()
        self.assert_authorization_HTTP_403_FORBIDDEN(
            *self.get_crud_methods()
        )

    def test_retrieve_all_items(self):
        """
        Test retrieve all items in any attribute.
        Test if items don't exist.
        """

        self.set_admin_authorization()

        # response = self.client.get(self)

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

    def get_crud_methods(self):
        return (lambda: self.client.get(self.attribute_items_endpoint),
                lambda: self.client.post(self.attribute_items_endpoint, data=self.new_items),
                lambda: self.client.put(f"{self.attribute_items_endpoint}{self.get_item_id()}/",
                                        data=self.item_saved_data),
                lambda: self.client.delete(f"{self.attribute_items_endpoint}{self.get_item_id()}/"))

    def get_item_id(self):
        try:
            attribute = AttributeItem.objects.get(item=self.item_saved_name)
            return attribute.id
        except Attribute.DoesNotExist:
            return None
