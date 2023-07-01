from app.attributes.tests.faker.data import FakeAttribute as _Data
from app.attributes.tests.base_test_case import BaseTestCase
from app.attributes.models import Attribute, AttributeItem


class AttributeValueViewTest(BaseTestCase):
    """
    [*] Test access permissions for CRUD methods
    [] Test CRUD results base on the multi scenario
    [] Test Retrieve all items of an attribute
    [] Test delete multi items
    """
    attribute_items_endpoint = "/catalog/attribute-items/"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # populate database
        _Data().populate_attributes_items()

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
                lambda: self.client.post(self.attribute_items_endpoint),
                lambda: self.client.put(self.attribute_items_endpoint),
                lambda: self.client.delete(self.attribute_items_endpoint))

    def get_item_id(self):
        try:
            attribute = AttributeItem.objects.get(item=_Data.item_saved_name)
            return attribute.id
        except Attribute.DoesNotExist:
            return None
