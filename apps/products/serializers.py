from rest_framework import serializers
from apps.products.models import Product, ProductOption, ProductOptionItem, ProductVariant


class ProductOptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionItem
        fields = ['item']


class ProductOptionSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = ProductOption
        fields = ['name', 'items']


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'status', 'options']
