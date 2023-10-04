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

    def validate_options(self, options):
        """
        Merge dictionaries with the same "option_name" and make the "items" unique.
        Remove options with an empty "items" list.
        Check max 3 options per product.
        """
        merged_options = {}

        for option in options:
            option_name = option['option_name']
            items = option['items']

            if items:
                if option_name in merged_options:
                    merged_options[option_name].update(items)
                else:
                    merged_options[option_name] = set(items)

        unique_options = [
            {"option_name": option_name, "items": list(items)}
            for option_name, items in merged_options.items()
        ]
        if len(unique_options) > 3:
            raise serializers.ValidationError("A product can have a maximum of 3 options.")

        # I need to sort option-names and item-names, for use to compare two dict in `assertEqual` function in the tests
        for option in unique_options:
            option['items'] = sorted(option['items'])
        unique_options = sorted(unique_options, key=lambda x: x['option_name'])
        return unique_options

    def validate_status(self, value):
        """
        Validate the "status" field and return `draft` if it is invalid or not set
        """
        valid_statuses = [status[0] for status in Product.STATUS_CHOICES]
        if value not in valid_statuses:
            return 'draft'
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id']
