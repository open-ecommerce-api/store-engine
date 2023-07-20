from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.products.models import Product, ProductOption
from apps.products import serializers


# todo[] write a test for POST product.
# todo[] if admin wants to edit the options, so how to manage variants if it is in the order list?


@extend_schema_view(
    create=extend_schema(
        tags=["Product"],
        summary='Create a new product',
        description='Create a new product.',
    ),
    retrieve=extend_schema(
        tags=["Product"],
        summary='Retrieve a product',
        description='Retrieve a single product by `id`.',
    ),
    update=extend_schema(
        tags=["Product"],
        summary='Update a product',
        description="Update product detail.",
    ),
    destroy=extend_schema(
        tags=["Product"],
        summary='Delete a product',
        description='Delete a product.',
    ),
    list=extend_schema(
        tags=["Product"],
        summary='Retrieve a list of products',
        description='Retrieve a list of products.',
    )
)
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payload = serializer.validated_data
        product, options = Product.objects.create_product(**payload)

        response_data = {
            'product_id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'status': product.status,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'published_at': product.published_at,
            'options': options
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
