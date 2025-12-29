from django.urls import path
from client_panel.viewsets.views import (
    HomePage,
    ShopPage,
)

from client_panel.viewsets.auth import (
    LoginPage,
    RegisterPage,
    LogoutPage,
    ForgotPwdPage,
    SetPwdPage,
)

urlpatterns = [
    path("", HomePage.as_view(), name="home-page"),
    path("shop/", ShopPage.as_view(), name="shop-page"),
    # Auth 
    path("login/", LoginPage.as_view(), name="login-page"),
    path("register/", RegisterPage.as_view(), name="register-page"),
    path("logout/", LogoutPage.as_view(), name="logout-page"),
    path("forgot-password/", ForgotPwdPage.as_view(), name="fpwd-page"),
    path("set-password/", SetPwdPage.as_view(), name="spwd-page"),

    # Auth 
]