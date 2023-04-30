from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)


class Variant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class VariantItem(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='variant_items',
        verbose_name='variant_verbose'
    )
    item_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('variant', 'item_name')

    def __str__(self):
        return self.item_name


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product_media')


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    track_inventory = models.BooleanField(default=True)
    sku = models.CharField(max_length=255, unique=True)
