from app.attributes.models import Attribute, AttributeItem


class FakeAttribute:
    """
    Populates the database with initial data
    """

    attribute_color_items = ['red', 'green', 'black', 'blue']
    attribute_size_items = ['S', 'M', 'L', 'XL', 'XXL']
    attribute_material_items = ['Cotton', 'Nylon']

    attributes = {
        'color': attribute_color_items,
        'size': attribute_size_items,
        'material': attribute_material_items
    }

    def fill_attributes(self):
        self.populate_attributes_items()

    def populate_attributes(self):
        """
        Fil database by fake data
        """
        for attribute_name, _ in self.attributes.items():
            Attribute.objects.create(name=attribute_name)

    def populate_attributes_items(self):
        """
        Fil database by fake data
        """
        for attribute_name, item_list in self.attributes.items():
            attribute = Attribute.objects.create(name=attribute_name)

            # create a list of AttributeItem objects using a list comprehension
            item_objects = [AttributeItem(attribute=attribute, item=item) for item in item_list]

            # insert all the AttributeItem objects into the database in a single query
            AttributeItem.objects.bulk_create(item_objects)
