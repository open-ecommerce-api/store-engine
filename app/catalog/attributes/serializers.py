from rest_framework import serializers
from app.catalog.models import Attribute, AttributeItem


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField()
    attribute_id = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), source='attribute')

    class Meta:
        model = AttributeItem
        fields = ['id', 'item', 'attribute_id']


class AttributeMultiItemSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField())
    attribute_id = serializers.IntegerField()

    class Meta:
        model = AttributeItem
        fields = ['id', 'items', 'attribute_id']

    def validate(self, attrs):
        attribute_id = attrs.get('attribute_id')
        items = attrs.get('items')
        if not attribute_id:
            raise serializers.ValidationError('attribute ID is required')
        try:
            Attribute.objects.get(id=attribute_id)
        except Attribute.DoesNotExist:
            raise serializers.ValidationError('Attribute does not exist')
        if items is None:
            raise serializers.ValidationError('Items is required')
        return attrs


class AttributeItemUpdateSerializer(serializers.ModelSerializer):
    item = serializers.CharField()

    class Meta:
        model = AttributeItem
        fields = ['id', 'item']


class AttributeItemDeleteSerializer(serializers.Serializer):
    item_ids = serializers.ListField(child=serializers.IntegerField())
