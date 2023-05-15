from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Variant, VariantItem
from .serializers import VariantSerializer, VariantItemSerializer, VariantItemUpdateSerializer


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
    ),
    get_items_for_variant=extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve all items of a variant',
        description='Retrieve all items of a variant.',
    )
)
class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(methods=['get'], detail=True, url_path='items')
    def get_items_for_variant(self, request, pk=None):
        try:
            pk = int(pk)  # convert pk to an integer
        except ValueError:
            return Response({'detail': 'Variant ID should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        variant = get_object_or_404(Variant, pk=pk)
        variant_items = VariantItem.objects.filter(variant=variant)
        serializer = VariantItemSerializer(variant_items, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    create=extend_schema(
        tags=["Catalog - Variant"],
        summary='Create a new item',
        description='Create a new item for a variant.',
    ),
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
    ),
    list=extend_schema(
        tags=["Catalog - Variant"],
        summary='Retrieve all items',
        description='Retrieve all items in any variant.',
    ),
    create_variant_items=extend_schema(
        tags=["Catalog - Variant"],
        summary='Create multi items',
        description='Create multi items for a variant.',
    ),
    delete_variant_items=extend_schema(
        tags=["Catalog - Variant"],
        summary='Delete Multi Items',
        description='Delete multi items form a variant.',
    )
)
class VariantItemViewSet(viewsets.ModelViewSet):
    queryset = VariantItem.objects.all()
    serializer_class = VariantItemSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'update':
            return VariantItemUpdateSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        # disable `list` method; raise a '405 Method Not Allowed error'
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post'], detail=False, url_path='multi-items')
    def create_variant_items(self, request):
        variant_id = request.data.get('variant_id')
        items = request.data.get('items')
        if not variant_id:
            return Response({'detail': 'Variant ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            variant = Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            return Response({'detail': 'Variant does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if items is None:
            return Response({'detail': 'Items is required'}, status=status.HTTP_400_BAD_REQUEST)

        variant_items_data = [{'variant_id': variant.id, 'item_name': value} for value in items]
        serializer = VariantItemSerializer(data=variant_items_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False, url_path='delete-items')
    def delete_variant_items(self, request):
        item_ids = request.data.get('item_ids')
        if not item_ids:
            return Response({'detail': 'Item IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the variant items to be deleted using the given variant and item IDs
        variant_items = VariantItem.objects.filter(id__in=item_ids)

        # Delete the variant items
        count, _ = variant_items.delete()

        if count > 0:
            return Response({'detail': f'{count} variant items deleted successfully.'})
        return Response({'detail': 'No variant items found to delete.'}, status=status.HTTP_404_NOT_FOUND)
