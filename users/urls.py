from django.urls import path
from .views import RegisterView, LoginView, User_logout_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', User_logout_user, name='logout'),

]
