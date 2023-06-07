from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from catalog.models import AttributeValue, Attribute
from catalog.attributes import serializers


@extend_schema_view(
    create=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Create a new attribute',
        description='Create a new attribute.',
    ),
    retrieve=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve an attribute',
        description='Retrieve a single attribute by `id`.',
    ),
    update=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Update an attribute',
        description="Update an attribute's name.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Delete an attribute',
        description='Delete an attribute.',
    ),
    list=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve a list of attributes',
        description='Retrieve a list of attributes.',
    )
)
class AttributeView(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve all values of an attribute',
        description='Retrieve all values of an attribute.',
    )
    @action(methods=['get'], detail=True, url_path='values')
    def get_attribute_values(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            return Response({'detail': 'attributes ID should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        attribute = get_object_or_404(Attribute, pk=pk)
        attribute_values = AttributeValue.objects.filter(attribute=attribute)
        serializer = serializers.AttributeValueSerializer(attribute_values, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve a value',
        description='Retrieve a single value.',
    ),
    list=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve all values',
        description="Retrieve all values in any attribute.",
    ),
    update=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Update a value',
        description="Update a value.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Delete a value',
        description='Delete a single value in an attribute.',
    )
)
class AttributeValueView(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = serializers.AttributeValueSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.AttributeValueSerializer
        if self.action == 'create':
            return serializers.AttributeMultiValueSerializer
        return self.serializer_class

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Create a new value(s)',
        description='Create a new value(s) for an attribute.',
    )
    def create(self, request, *args, **kwargs):
        """
        Create one or multiple value.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attribute_id = serializer.validated_data['attribute_id']
        values = serializer.validated_data['values']

        attribute_values = [{'attribute_id': attribute_id, 'value': value} for value in values]
        serializer = serializers.AttributeValueSerializer(data=attribute_values, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Delete Multi Values',
        description='Delete multi Values form an attribute.',
        request=serializers.AttributeValueDeleteSerializer,
    )
    @action(methods=['post'], detail=False, url_path='delete-values')
    def delete_attribute_values(self, request):
        serializer = serializers.AttributeValueDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        value_ids = serializer.validated_data.get('value_ids')
        if not value_ids:
            return Response({'detail': 'Value IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the attribute values to be deleted using the given value IDs
        attribute_values = AttributeValue.objects.filter(id__in=value_ids)

        # Delete the attribute values
        count, _ = attribute_values.delete()

        if count > 0:
            return Response({'detail': f'{count} attribute values deleted successfully.'})
        return Response({'detail': 'No attribute values found to delete.'}, status=status.HTTP_404_NOT_FOUND)
