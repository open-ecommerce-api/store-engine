from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.products.models import Product
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

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        # todo[] create variants

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        product, options = Product.objects.create_product(**payload)

        response_body = {
            'product_id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'status': product.status,
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'options': options
        }

        return Response(response_body, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        # todo[] get a product
        # todo[] get options of product
        # todo[] get variant of product
        # todo[] combine all and return in response

        try:
            pk = int(pk)
        except ValueError:
            return Response({'detail': 'product id should be integer'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=pk)
        options = Product.objects.retrieve_options(product)
        # variants= Product.objects.retrieve_variants(product)

        response_body = {
            'product_id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'status': product.status,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'published_at': product.published_at,
            'options': options
        }

        return Response(response_body, status=status.HTTP_200_OK)

    # product, options, variants = Product.objects.get(**payload)
    #
    # response_body = {
    #     'product_id': product.id,
    #     'product_name': product.product_name,
    #     'description': product.description,
    #     'status': product.status,
    #     'created_at': product.created_at,
    #     'updated_at': product.updated_at,
    #     'published_at': product.published_at,
    #     'options': options
    # }
    #
    # return Response(response_body, status=status.HTTP_200_OK)
