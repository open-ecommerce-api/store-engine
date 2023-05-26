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


class ProductOption(models.Model):
    """
    The custom product properties.
    For example, Size, Color, and Material. Each product can have up to 3 options, and each option value can be
    up to 255 characters. Product variants are made of up combinations of option values. Options cannot be created
    without values. To create new options, a variant with an associated option value also needs to be created.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductOptionValue(models.Model):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        # related_name='variant_items',
        # verbose_name='variant_verbose'
    )
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    track_inventory = models.BooleanField(default=True)
    sku = models.CharField(max_length=255, unique=True)
