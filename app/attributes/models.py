from django.db import models


class Attribute(models.Model):
    """
    In e-commerce, "attributes" and "options" collaborate to create a customizable product offering.
    By defining relevant attributes and their items, admins can configure products to meet specific needs, enhancing
    the user experience and enabling customers to find desired variations.

    An "attribute list group" streamlines the process by allowing admins to add product options and create variants
    efficiently, saving time when repetitive attributes need to be included.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AttributeItem(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)

    class Meta:
        unique_together = ('attribute', 'item')


class AttributeQueryset:
    ...


class AttributeItemQueryset:

    @staticmethod
    def delete_items_by_id(item_ids):
        """
        Filter the attribute items to be deleted using the given item IDs
        """
        attribute_items = AttributeItem.objects.filter(id__in=item_ids)

        # Delete the attribute items
        count, _ = attribute_items.delete()
        return count
