from django.urls import path, include
from rest_framework import routers
from apps.attributes.views import AttributeView, AttributeItemView

router = routers.DefaultRouter()
router.register(r'attributes', AttributeView)
router.register(r'attribute-items', AttributeItemView)

urlpatterns = [
    path('', include(router.urls)),
]
