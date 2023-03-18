from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.ProductAdd.as_view(), name="product_add"),
    path("<int:product_id>/images/add/", views.ProductAddMedia.as_view(), name="product_add_media"),
]
