from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, max_length=500)

    # an introduction of the product, Support HTML formatting.
    introduction = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True, )

    # Model Meta is basically used to change the behavior of your model fields like changing order options
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name