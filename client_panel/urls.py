from django.urls import path
from client_panel.views import HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="home-page"),
]