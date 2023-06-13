from rest_framework import serializers
from catalog.models import ProductOption, ProductOptionValue, Product


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'


class ProductOptionValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField()
    option_id = serializers.PrimaryKeyRelatedField(queryset=ProductOption.objects.all(), source='option')

    class Meta:
        model = ProductOptionValue
        fields = ['id', 'value', 'option_id']


class ListField(serializers.ListField):
    def to_representation(self, data):
        return data

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data
        raise serializers.ValidationError('Invalid input type: expected a list.')


class OptionMultiValueSerializer(serializers.ModelSerializer):
    values = serializers.ListField(child=serializers.CharField())
    option_id = serializers.IntegerField()

    class Meta:
        model = ProductOptionValue
        fields = ['id', 'values', 'option_id']

    def validate(self, attrs):
        option_id = attrs.get('option_id')
        values = attrs.get('values')
        if not option_id:
            raise serializers.ValidationError('Option ID is required')
        try:
            ProductOption.objects.get(id=option_id)
        except ProductOption.DoesNotExist:
            raise serializers.ValidationError('Option does not exist')
        if values is None:
            raise serializers.ValidationError('Values is required')
        return attrs


class OptionValueUpdateSerializer(serializers.ModelSerializer):
    value = serializers.CharField()

    class Meta:
        model = ProductOptionValue
        fields = ['id', 'value']


class OptionValueDeleteSerializer(serializers.Serializer):
    value_ids = serializers.ListField(child=serializers.IntegerField())


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
