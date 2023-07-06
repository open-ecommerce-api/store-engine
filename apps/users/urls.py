from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/confirm/<str:token>', views.ConfirmSignupView.as_view(), name='confirm_signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/<str:token>', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change_email/', views.ChangeEmailView.as_view(), name='change_email'),
]
