from django.urls import path, include
from rest_framework import routers
from .views import VariantViewSet, VariantItemViewSet

router = routers.DefaultRouter()
router.register(r'variants', VariantViewSet)
router.register(r'variant-items', VariantItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
