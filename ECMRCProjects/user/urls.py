from django.urls import path
from .views import UserSignUp, UserLogin

urlpatterns = [
    path('registration', UserSignUp.as_view(), name="user_signup"),
    path('login', UserLogin.as_view(), name='user_login')
]