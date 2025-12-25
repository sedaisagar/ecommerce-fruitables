from django.urls import path
from admin_panel.views import AdminDashBoardPage

urlpatterns = [
    path("", AdminDashBoardPage.as_view(), name="admin-dashboard"),
]