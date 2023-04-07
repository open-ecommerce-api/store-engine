from django.db import models


class ProductType(models.Model):
    """
    `ProductType` in ecommerce refers to the category or type of product being sold.
    It is a way of organizing and classifying products based on their characteristics and intended use.
    For example, in a fashion ecommerce store, the product types could be clothing, shoes, and accessories.
    In a grocery ecommerce store, the product types could be fresh produce, canned goods, and snacks.
    Product types are important in ecommerce because they help customers quickly and easily find the products they are
    looking for, and they also help ecommerce businesses manage their inventory and product listings.
    By using product types, businesses can more effectively track their sales and make data-driven decisions about
    which types of products to stock and promote.
    """
    name = models.CharField(max_length=255)
