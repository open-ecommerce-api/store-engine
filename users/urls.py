from django.urls import path
from .views import RegisterView, LoginView, User_logout_user, adminLogin, ChangePasswordView, ResetPassword

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', User_logout_user, name='logout'),

    path('adminlogin/', adminLogin, name='adminlogin' ),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPassword.as_view(),name='reset-password'), 

]
