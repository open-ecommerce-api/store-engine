from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from products.models import Product, ProductMedia
from .serializers import ProductAddSerializer, ProductAddMediaSerializer


class ProductAdd(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = [IsAdminUser]


class ProductAddMedia(generics.CreateAPIView):
    serializer_class = ProductAddMediaSerializer
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        # use this method to get one object by ID from database
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        media = ProductMedia.objects.filter(product=product_id)
        return media
