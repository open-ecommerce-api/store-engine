from django.urls import path, include
from rest_framework import routers
from .views import VariantViewSet, VariantItemViewSet

router = routers.DefaultRouter()
router.register(r'variants', VariantViewSet)
router.register(r'variant-items', VariantItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('multi-items/', VariantMultiItemView.as_view(), name='create_variant_items'),
]
