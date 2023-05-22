from rest_framework import serializers
from .models import Variant, VariantItem


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class VariantItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField()
    variant_id = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all(), source='variant')

    class Meta:
        model = VariantItem
        fields = ['id', 'item_name', 'variant_id']


class ListField(serializers.ListField):
    def to_representation(self, data):
        return data

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data
        raise serializers.ValidationError('Invalid input type: expected a list.')


class VariantMultiItemSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField())
    variant_id = serializers.IntegerField()

    class Meta:
        model = VariantItem
        fields = ['id', 'items', 'variant_id']

    def validate(self, attrs):
        variant_id = attrs.get('variant_id')
        items = attrs.get('items')
        if not variant_id:
            raise serializers.ValidationError('Variant ID is required')
        try:
            Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            raise serializers.ValidationError('Variant does not exist')
        if items is None:
            raise serializers.ValidationError('Items is required')
        return attrs


class VariantItemUpdateSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField()

    class Meta:
        model = VariantItem
        fields = ['id', 'item_name']


class DeleteVariantItemsSerializer(serializers.Serializer):
    item_ids = serializers.ListField(child=serializers.IntegerField())
