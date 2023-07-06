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
    save selected options with it's items
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


class ProductOptionItem(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)

    class Meta:
        unique_together = ('option', 'item')

    def __str__(self):
        return self.item


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product_media')


class ProductVariant(models.Model):
    """
    Product variants are created by combining different option items.
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
    # save each option-item-id
    # ---------------------------------------------------------------------------------------------
    # option1 = models.ForeignKey(ProductOptionItem, on_delete=models.CASCADE, null=True, blank=True)
    # option2 = models.ForeignKey(ProductOptionItem, on_delete=models.CASCADE, null=True, blank=True)
    # option3 = models.ForeignKey(ProductOptionItem, on_delete=models.CASCADE, null=True, blank=True)
    # ---------------------------------------------------------------------------------------------
