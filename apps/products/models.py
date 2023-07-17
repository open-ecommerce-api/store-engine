from django.db import models


class ProductQuerySet(models.QuerySet):

    def create_product(self, name, description, options):
        """
        [*] get selected attributes
        [*] generate options
        [*] save options

        [] generate variants: by options combination, max is 3 options
        [] save variants
        """

        # create a product
        product = self.model.objects.create(
            name=name,
            description=description,
        )

        # create product options
        for option in options:
            product_option = ProductOption.objects.create(
                product=product,
                name=option['name'],
            )

            for item in option['items']:
                ProductOptionItem.objects.create(
                    option=product_option,
                    item=item,
                )

        # create product variants

        return product


class Product(models.Model):
    """
    The Product resource lets you update and create products in a merchant's store.
    You can use product variants with the Product resource to create or update different versions of the same product.
    You can also add or update product images.
    """
    name = models.CharField(max_length=255)

    # A description of the product. Supports HTML formatting.
    description = models.TextField()

    STATUS_CHOICES = [

        # The product is ready to sell and is available to customers on the online store, sales channels, and apps.
        ('active', 'Active'),

        # The product is no longer being sold and isn't available to customers on sales channels and apps.
        ('archived', 'Archived'),

        # The product isn't ready to sell and is unavailable to customers on sales channels and apps.
        ('draft', 'Draft'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # the date and time when the product was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # The date and time when the product was last modified.
    # A product's updated_at value can change for different reasons.
    # For example, the inventory adjustment is counted as an update.
    updated_at = models.DateTimeField(auto_now=True)

    # The date and time when the product was published.
    published_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductOption(models.Model):
    """
    To enhance search ability, include descriptive information like "Color" or "Size" for customers to use when
    searching on your store.
    Each product can have a maximum of 3 options, such as Size, Color, and Material.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return self.name


class ProductOptionItem(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)

    class Meta:
        unique_together = ('option', 'item')

    def __str__(self):
        return self.item


class ProductVariant(models.Model):
    """
    Product variants are created by combining different option items.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)

    option_item_1 = models.ForeignKey(
        ProductOptionItem, related_name='option_item_1', on_delete=models.CASCADE, null=True, blank=True)

    option_item_2 = models.ForeignKey(
        ProductOptionItem, related_name='option_item_2', on_delete=models.CASCADE, null=True, blank=True)

    option_item_3 = models.ForeignKey(
        ProductOptionItem, related_name='option_item_3', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class ProductMedia(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     file = models.ImageField(upload_to='product_media')
