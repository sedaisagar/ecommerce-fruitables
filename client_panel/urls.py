from django.urls import path
from client_panel.viewsets.views import (
    HomePage,

)

from client_panel.viewsets.auth import (
    LoginPage,
    RegisterPage,
)

urlpatterns = [
    path("", HomePage.as_view(), name="home-page"),
    # Auth 
    path("login/", LoginPage.as_view(), name="login-page"),
    path("register/", RegisterPage.as_view(), name="register-page"),
    # Auth 
]