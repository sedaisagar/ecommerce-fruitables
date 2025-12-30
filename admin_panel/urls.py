from django.urls import path
from admin_panel.views import AdminDashBoardPage

from admin_panel.viewsets.category import (
    CategoryList,
    CategoryCreate,
    CategoryEdit,
    CategoryDelete,
)
urlpatterns = [
    path("", AdminDashBoardPage.as_view(), name="admin-dashboard"),
    # Category
    path("categories/", CategoryList.as_view(), name="admin-categories"),
    path("categories/create/", CategoryCreate.as_view(), name="admin-categories-create"),
    path("categories/edit/<str:pk>/", CategoryEdit.as_view(), name="admin-categories-edit"),
    path("categories/delete/<str:pk>/", CategoryDelete.as_view(), name="admin-categories-delete"),

]