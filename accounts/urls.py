from django.urls import path
from .views import *

urlpatterns = [
    path('login/', OTPLoginView.as_view(), name='OTPLoginView'),
    path('logout/', User_logout, name='logoutclient'),
]
