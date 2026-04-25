from django.urls import path
from rest_framework.urls import app_name

from .views import LoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="login"),
    path("login/", LoginView.as_view(), name="register"),
]
