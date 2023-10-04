from django.urls import path, include
from rest_framework import routers
from apps.products.views import ProductView

router = routers.DefaultRouter()
router.register(r'products', ProductView)

urlpatterns = [
    path('', include(router.urls)),
]
