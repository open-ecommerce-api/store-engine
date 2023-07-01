from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app.catalog.models import Product, ProductOption, ProductOptionItem
from . import serializers


@extend_schema_view(
    create=extend_schema(
        tags=["Catalog - Option"],
        summary='Create a new Option',
        description='Create a new Option.',
    ),
    retrieve=extend_schema(
        tags=["Catalog - Option"],
        summary='Retrieve an Option',
        description='Retrieve a single Option by `id`.',
    ),
    update=extend_schema(
        tags=["Catalog - Option"],
        summary='Update an Option',
        description="Update an Option's name.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Option"],
        summary='Delete an Option',
        description='Delete an Option.',
    ),
    list=extend_schema(
        tags=["Catalog - Option"],
        summary='Retrieve a list of Options',
        description='Retrieve a list of Options.',
    )
)
class ProductOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductOption.objects.all()
    serializer_class = serializers.ProductOptionSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        tags=["Catalog - Option"],
        summary='Retrieve all values of an Option',
        description='Retrieve all values of an Option.',
    )
    @action(methods=['get'], detail=True, url_path='values')
    def get_option_values(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            return Response({'detail': 'Option ID should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        option = get_object_or_404(ProductOption, pk=pk)
        option_values = ProductOptionItem.objects.filter(option=option)
        serializer = serializers.ProductOptionValueSerializer(option_values, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Catalog - Option"],
        summary='Retrieve a value',
        description='Retrieve a single value.',
    ),
    list=extend_schema(
        tags=["Catalog - Option"],
        summary='Retrieve all values',
        description="Retrieve all values in any option.",
    ),
    update=extend_schema(
        tags=["Catalog - Option"],
        summary='Update a value',
        description="Update a value.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Option"],
        summary='Delete a value',
        description='Delete a single value in an option.',
    )
)
class ProductOptionValueViewSet(viewsets.ModelViewSet):
    queryset = ProductOptionItem.objects.all()
    serializer_class = serializers.ProductOptionValueSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.OptionValueUpdateSerializer
        if self.action == 'create':
            return serializers.OptionMultiValueSerializer
        return self.serializer_class

    @extend_schema(
        tags=["Catalog - Option"],
        summary='Create a new value(s)',
        description='Create a new value(s) for an option.',
    )
    def create(self, request, *args, **kwargs):
        """
        Create one or multiple value.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        option_id = serializer.validated_data['option_id']
        values = serializer.validated_data['values']

        option_values = [{'option_id': option_id, 'value': value} for value in values]
        serializer = serializers.ProductOptionValueSerializer(data=option_values, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["Catalog - Option"],
        summary='Delete Multi Values',
        description='Delete multi Values form an option.',
        request=serializers.OptionValueDeleteSerializer,
    )
    @action(methods=['post'], detail=False, url_path='delete-values')
    def delete_option_values(self, request):
        serializer = serializers.OptionValueDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        value_ids = serializer.validated_data.get('value_ids')
        if not value_ids:
            return Response({'detail': 'Value IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the option values to be deleted using the given value IDs
        option_values = ProductOptionItem.objects.filter(id__in=value_ids)

        # Delete the option values
        count, _ = option_values.delete()

        if count > 0:
            return Response({'detail': f'{count} option values deleted successfully.'})
        return Response({'detail': 'No option values found to delete.'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    create=extend_schema(
        tags=["Catalog - Product"],
        summary='Create a new product',
        description='Create a new product.',
    ),
    retrieve=extend_schema(
        tags=["Catalog - Product"],
        summary='Retrieve a single product',
        description='Retrieve a single product.',
    ),
    list=extend_schema(
        tags=["Catalog - Product"],
        summary='Retrieve a list of products',
        description="Retrieve a list of products.",
    ),
    update=extend_schema(
        tags=["Catalog - Product"],
        summary='Update a product',
        description="Update a product.",
    ),
    destroy=extend_schema(
        tags=["Catalog - Product"],
        summary='Delete a product',
        description='Delete a product.',
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']
