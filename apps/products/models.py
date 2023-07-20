from django.db import models


class ProductQuerySet(models.QuerySet):

    def create_product(self, **data):
        """
        todo[*] get selected attributes
        todo[*] generate options
        todo[*] save options

        todo[] generate variants: by options combination, max is 3 options
        todo[] save variants
        """

        try:
            # pop options, because the Product model doesn't have `options` field
            options = data.pop('options')
        except KeyError:
            options = []

        # create a product
        product = self.model.objects.create(**data)

        # create product options
        product_options = self.__create_product_options(product, options)

        # create product variants

        return product, product_options

    def __create_product_options(self, product, options):
        product_options = []

        if product_options:
            for option in options:

                new_option = ProductOption.objects.create(
                    product=product,
                    option_name=option['option_name'],
                )

                items = []
                for item in option['items']:
                    new_item = ProductOptionItem.objects.create(
                        option=new_option,
                        item_name=item,
                    )
                    items.append({
                        'item_id': new_item.id,
                        'item_name': new_item.item_name
                    })

                product_options.append({
                    'options_id': new_option.id,
                    'option_name': new_option.option_name,
                    'items': items
                })
        else:
            product_options = None

        return product_options


class Product(models.Model):
    """
    The Product resource lets you update and create products in a merchant's store.
    You can use product variants with the Product resource to create or update different versions of the same product.
    You can also add or update product images.
    """
    product_name = models.CharField(max_length=255)

    # A description of the product. Supports HTML formatting.
    # todo [] makesure the description can save and retrieve the html content
    description = models.TextField(blank=True)

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
    updated_at = models.DateTimeField(blank=True, null=True)

    # The date and time when the product was published.
    published_at = models.DateTimeField(blank=True, null=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        # Check if the status field is empty or None or other names
        if not self.status or self.status != ('active', 'archived', 'draft'):
            self.status = 'draft'
        super().save(*args, **kwargs)


class ProductOption(models.Model):
    """
    To enhance search ability, include descriptive information like "Color" or "Size" for customers to use when
    searching on your store.
    Each product can have a maximum of 3 options, such as Size, Color, and Material.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('product', 'option_name')

    def __str__(self):
        return self.option_name


class ProductOptionItem(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('option', 'item_name')

    def __str__(self):
        return self.item_name


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
