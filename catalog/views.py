from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Variant, VariantItem
from . import serializers


@extend_schema_view(
    create=extend_schema(
        tags=["Catalog - Variant"],
        summary='Create a new variant',
        description='Create a new variant.',
    ),
    retrieve=extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve a variant',
        description='Retrieve a single variant by `id`.',
    ),
    update=extend_schema(
        tags=["Catalog - Variant"],
        summary='Update a variant',
        description="Update a variant's name.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Variant"],
        summary='Delete a variant',
        description='Delete a variant.',
    ),
    list=extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve a list of variants',
        description='Retrieve a list of variants.',
    )
)
class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = serializers.VariantSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve all items of a variant',
        description='Retrieve all items of a variant.',
    )
    @action(methods=['get'], detail=True, url_path='items')
    def get_items_for_variant(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            return Response({'detail': 'Variant ID should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        variant = get_object_or_404(Variant, pk=pk)
        variant_items = VariantItem.objects.filter(variant=variant)
        serializer = serializers.VariantItemSerializer(variant_items, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve an item',
        description='Retrieve a single item.',
    ),
    update=extend_schema(
        tags=["Catalog - Variant"],
        summary='Update an item',
        description="Update an item's name.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Variant"],
        summary='Delete an item',
        description='Delete a single item in a variant.',
    )
)
class VariantItemViewSet(viewsets.ModelViewSet):
    queryset = VariantItem.objects.all()
    serializer_class = serializers.VariantItemSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.VariantItemUpdateSerializer
        if self.action == 'create':
            return serializers.VariantMultiItemSerializer
        return self.serializer_class

    @extend_schema(
        tags=["Catalog - Variant"],
        summary='Create a new item(s)',
        description='Create a new item for a variant.',
    )
    def create(self, request, *args, **kwargs):
        """
        Create one or multiple items.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant_id = serializer.validated_data['variant_id']
        items = serializer.validated_data['items']

        variant_items_data = [{'variant_id': variant_id, 'item_name': value} for value in items]
        serializer = serializers.VariantItemSerializer(data=variant_items_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["Catalog - Variant"],
        summary='Delete Multi Items',
        description='Delete multi items form a variant.',
        request=serializers.DeleteVariantItemsSerializer,
    )
    @action(methods=['post'], detail=False, url_path='delete-items')
    def delete_variant_items(self, request):
        serializer = serializers.DeleteVariantItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_ids = serializer.validated_data.get('item_ids')
        if not item_ids:
            return Response({'detail': 'Item IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the variant items to be deleted using the given variant and item IDs
        variant_items = VariantItem.objects.filter(id__in=item_ids)

        # Delete the variant items
        count, _ = variant_items.delete()

        if count > 0:
            return Response({'detail': f'{count} variant items deleted successfully.'})
        return Response({'detail': 'No variant items found to delete.'}, status=status.HTTP_404_NOT_FOUND)
