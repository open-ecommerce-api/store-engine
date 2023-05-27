from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet
from catalog.attributes.views import AttributeView, AttributeValueView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'attributes', AttributeView)
router.register(r'attribute-values', AttributeValueView)

urlpatterns = [
    path('', include(router.urls)),
]
