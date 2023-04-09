from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
]
