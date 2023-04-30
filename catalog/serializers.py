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


class VariantItemUpdateSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField()
    variant_id = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all(), source='variant', required=False)

    class Meta:
        model = VariantItem
        fields = ['id', 'item_name', 'variant_id']

        # you can remove the variant field from the PUT request body, and it will not be required during updates
        read_only_fields = ['variant']
