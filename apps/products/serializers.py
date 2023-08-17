from rest_framework import serializers

from apps.products.models import Product, ProductOption, ProductOptionItem, ProductVariant


class ProductOptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionItem
        fields = ['item_name']


class ProductOptionSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = ProductOption
        fields = ['option_name', 'items']


class ProductCreateSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, required=False)
    status = serializers.CharField(max_length=10, allow_blank=True, required=False)

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'status', 'options']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id']
