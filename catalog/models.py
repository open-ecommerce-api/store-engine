from django.db import models


class ProductType(models.Model):
    """
    A categorization for the product used for filtering and searching products.
    """
    name = models.CharField(max_length=255)


class Product(models.Model):
    # product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)

    """
    save selected options with it's values
    """

    # solution
    selected_options = models.JSONField(blank=True, null=True)
    #


class ProductOption(models.Model):
    """
    To enhance search ability, include descriptive information like "Material" or "Brand" for customers to use when
    searching on your store.
    Each product can have a maximum of 3 options, such as Size, Color, and Material.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductOptionValue(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('option', 'value')

    def __str__(self):
        return self.value


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product_media')


class ProductVariant(models.Model):
    """
    Product variants are created by combining different option values.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variant = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=255, unique=True)
    # track_inventory = models.BooleanField(default=True)

    """
    save variant combination
    """

    # solution 1
    # save each option-value-id
    # ---------------------------------------------------------------------------------------------
    # option1 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True)
    # option2 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True)
    # option3 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True)
    # ---------------------------------------------------------------------------------------------


class Attribute(models.Model):
    """
    In e-commerce, "attributes" and "options" collaborate to create a customizable product offering.
    By defining relevant attributes and their values, admins can configure products to meet specific needs, enhancing
    the user experience and enabling customers to find desired variations.

    An "attribute list group" streamlines the process by allowing admins to add product options and create variants
    efficiently, saving time when repetitive attributes need to be included.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('attribute', 'value')
