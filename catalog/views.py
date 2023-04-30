from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Variant, VariantItem
from .serializers import VariantSerializer, VariantItemSerializer, VariantItemUpdateSerializer


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

    # This is a temporary comment;
    # I override this method just to show how adding api documentation in `ViewSet`:
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html#customization-by-using-extend-schema

    # @extend_schema(request=VariantSerializer, responses={201: VariantSerializer})
    # def create(self, request, *args, **kwargs):
    #     """
    #     Create a new variant.
    #
    #     Returns the created variant.
    #     """
    #     return super().create(request, *args, **kwargs)


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
