from rest_framework import serializers
from catalog.models import Attribute, AttributeValue


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField()
    attribute_id = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), source='attribute')

    class Meta:
        model = AttributeValue
        fields = ['id', 'value', 'attribute_id']


class AttributeMultiValueSerializer(serializers.ModelSerializer):
    values = serializers.ListField(child=serializers.CharField())
    attribute_id = serializers.IntegerField()

    class Meta:
        model = AttributeValue
        fields = ['id', 'values', 'attribute_id']

    def validate(self, attrs):
        attribute_id = attrs.get('attribute_id')
        values = attrs.get('values')
        if not attribute_id:
            raise serializers.ValidationError('attribute ID is required')
        try:
            Attribute.objects.get(id=attribute_id)
        except Attribute.DoesNotExist:
            raise serializers.ValidationError('Attribute does not exist')
        if values is None:
            raise serializers.ValidationError('Values is required')
        return attrs


class AttributeValueUpdateSerializer(serializers.ModelSerializer):
    value = serializers.CharField()

    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeValueDeleteSerializer(serializers.Serializer):
    value_ids = serializers.ListField(child=serializers.IntegerField())
