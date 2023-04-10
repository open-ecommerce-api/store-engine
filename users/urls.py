from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/confirm/<str:token>', views.ConfirmSignupView.as_view(), name='confirm_signup'),
]
