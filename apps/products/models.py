from itertools import product as options_combination
from typing import Optional, List

from django.db import models
from djmoney.models.fields import MoneyField


class ProductQuerySet(models.QuerySet):
    product = None
    options = []
    options_data = []
    variants = []

    def create_product(self, **data):
        """
        todo[] generate variants: by options combination, max is 3 options
        """

        try:
            # pop options, because the Product model doesn't have `options` field
            self.options_data = data.pop('options')
        except KeyError:
            ...

        # create a product
        self.product = self.model.objects.create(**data)

        # create product options
        self.options = self.__create_product_options()

        # create product variants
        self.variants = self.__create_variants()

        return self.product, self.options, self.variants

    def __create_product_options(self):
        """
        Create new option if it doesn't exist and update its items,
        and ensures that options are uniq in a product and also items in each option are uniq.
        """

        if self.options_data:
            for option in self.options_data:
                new_option = ProductOption.objects.create(product=self.product, option_name=option['option_name'])
                for item in option['items']:
                    ProductOptionItem.objects.create(option=new_option, item_name=item)
            return self.retrieve_options(self.product.id)
        else:
            return None

    def __create_variants(self):
        """
        Create a default variant or crete variants by options combination
        """

        if self.options:
            # create variants by options combination (variant product)
            variants = []
            option_items = [option["items"] for option in self.options_data]
            variants = list(options_combination(*option_items))
            # for _ in variants:
            #     print(_)
            # variants = ProductVariant.objects.create()
        else:
            # set a default variant (simple product)
            ProductVariant.objects.create(product=self.product)

        return self.retrieve_variants(self.product)

    def retrieve_options(self, product_id) -> Optional[List[dict]]:
        """
        Get all options of a product
        """
        product_options = []
        options = ProductOption.objects.filter(product=product_id)
        for option in options:
            items = ProductOptionItem.objects.filter(option=option)
            product_options.append({
                'options_id': option.id,
                'option_name': option.option_name,
                'items': [{'item_id': item.id, 'item_name': item.item_name} for item in items]
            })
        if product_options:
            return product_options
        else:
            return None

    def retrieve_variants(self, product_id) -> Optional[List[dict]]:
        """
        Get all variants of a product
        """
        product_variants = []
        variants = ProductVariant.objects.filter(product=product_id)
        for variant in variants:
            product_variants.append(
                {
                    "variant_id": variant.id,
                    "product_id": variant.product.id,
                    "price": {
                        'amount': str(variant.price.amount),
                        'currency': str(variant.price.currency)
                    },
                    "stock": variant.stock,
                    "option1": variant.option1,
                    "option2": variant.option2,
                    "option3": variant.option3,
                    "created_at": variant.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": variant.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                })
        return product_variants


class Product(models.Model):
    """
    The Product resource lets you update and create products in a merchant's store.
    You can use product variants with the Product resource to create or update different versions of the same product.
    You can also add or update product images.
    """
    product_name = models.CharField(max_length=255)

    # A description of the product. Supports HTML formatting.
    # TODO makesure the description can save and retrieve the html content
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

    # def save(self, *args, **kwargs):
    # Check if the status field is empty or None or other names
    # if not self.status or self.status != ('active', 'archived', 'draft'):
    #     self.status = 'draft'
    # super().save(*args, **kwargs)


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
    price = MoneyField(max_digits=12, decimal_places=2, default_currency='USD', default=0)
    stock = models.IntegerField(default=0)

    option1 = models.ForeignKey(
        ProductOptionItem, related_name='option1', on_delete=models.CASCADE, null=True, blank=True)

    option2 = models.ForeignKey(
        ProductOptionItem, related_name='option2', on_delete=models.CASCADE, null=True, blank=True)

    option3 = models.ForeignKey(
        ProductOptionItem, related_name='option3', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class ProductMedia(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     file = models.ImageField(upload_to='product_media')
