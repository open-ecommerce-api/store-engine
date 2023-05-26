from django.urls import path, include
from rest_framework import routers
from .views import ProductOptionViewSet, ProductOptionValueViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'options', ProductOptionViewSet)
router.register(r'option-values', ProductOptionValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
