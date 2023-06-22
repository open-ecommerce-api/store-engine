from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app.catalog.models import AttributeItem, Attribute
from app.catalog.attributes import serializers


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

    def list(self, request, *args, **kwargs):
        attributes = self.get_queryset()

        if attributes.exists():
            serializer = self.get_serializer(attributes, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No attributes found.'}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve all items of an attribute',
        description='Retrieve all items of an attribute.',
    )
    @action(methods=['get'], detail=True, url_path='items')
    def get_attribute_items(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            return Response({'detail': 'attributes ID should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        attribute = get_object_or_404(Attribute, pk=pk)
        attribute_items = AttributeItem.objects.filter(attribute=attribute)
        serializer = serializers.AttributeItemSerializer(attribute_items, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve an item',
        description='Retrieve a single item.',
    ),
    list=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Retrieve all items',
        description="Retrieve all items in any attribute.",
    ),
    update=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Update a item',
        description="Update a item.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Attribute"],
        summary='Delete a item',
        description='Delete a single item in an attribute.',
    )
)
class AttributeItemView(viewsets.ModelViewSet):
    queryset = AttributeItem.objects.all()
    serializer_class = serializers.AttributeItemSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.AttributeItemSerializer
        if self.action == 'create':
            return serializers.AttributeMultiItemSerializer
        return self.serializer_class

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Create a new item(s)',
        description='Create a new item(s) for an attribute.',
    )
    def create(self, request, *args, **kwargs):
        """
        Create one or multiple item.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attribute_id = serializer.validated_data['attribute_id']
        items = serializer.validated_data['items']

        attribute_items = [{'attribute_id': attribute_id, 'item': value} for value in items]
        serializer = serializers.AttributeItemSerializer(data=attribute_items, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["Catalog - Attribute"],
        summary='Delete multi items',
        description='Delete multi items form an attribute.',
        request=serializers.AttributeItemDeleteSerializer,
    )
    @action(methods=['post'], detail=False, url_path='delete-items')
    def delete_attribute_items(self, request):
        serializer = serializers.AttributeItemDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_ids = serializer.validated_data.get('item_ids')
        if not item_ids:
            return Response({'detail': 'Item IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the attribute items to be deleted using the given item IDs
        attribute_items = AttributeItem.objects.filter(id__in=item_ids)

        # Delete the attribute items
        count, _ = attribute_items.delete()

        if count > 0:
            return Response({'detail': f'{count} attribute items deleted successfully.'})
        return Response({'detail': 'No attribute items found to delete.'}, status=status.HTTP_404_NOT_FOUND)
