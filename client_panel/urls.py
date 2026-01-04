from django.urls import path, include

from client_panel.viewsets.dashboard import (
    ClientDashBoardView,
    ClientCartView,
    ClientCheckOutView,
)

from client_panel.viewsets.views import (
    HomePage,
    ShopPage,
    ShopDetailPage,
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
    path("shop/<str:slug>/", ShopDetailPage.as_view(), name="shop-detail"),
    # Auth 
    path("login/", LoginPage.as_view(), name="login-page"),
    path("register/", RegisterPage.as_view(), name="register-page"),
    path("logout/", LogoutPage.as_view(), name="logout-page"),
    path("forgot-password/", ForgotPwdPage.as_view(), name="fpwd-page"),
    path("set-password/", SetPwdPage.as_view(), name="spwd-page"),
    # Client Dashboard
    path("user/", include(
        [
            path("dashboard/", ClientDashBoardView.as_view(), name="client-dash"),
            path("cart/", ClientCartView.as_view(), name="client-cart"),
            path("checkout/", ClientCheckOutView.as_view(), name="client-checkout"),
        ]
    )) 

]