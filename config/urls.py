"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    # to show a login button in a django rest framework navbar, you must set this route, and add a
    # `DEFAULT_AUTHENTICATION_CLASSES` config in setting file.
    path('api-auth/', include('rest_framework.urls')),

    # path('products/', include('products.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # need to generate swagger-ui
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc", ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # allows us to access media by url
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
