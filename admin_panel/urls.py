from django.urls import path
from admin_panel.views import AdminDashBoardPage

from admin_panel.viewsets.category import (
    CategoryList,
    CategoryCreate,
    CategoryEdit,
    CategoryDelete,
    CategoryDetail,
)

from admin_panel.viewsets.product import (
    ProductsList,
    ProductsCreate,
    ProductsEdit,
    ProductsDelete,
    ProductsDetail,
)
from admin_panel.viewsets.pages import (
    DynamicPagesList,
    DynamicPagesCreate,
    DynamicPagesEdit,
    DynamicPagesDelete,
    DynamicPagesDetail,
)
urlpatterns = [
    path("", AdminDashBoardPage.as_view(), name="admin-dashboard"),
    # Category
    path("categories/", CategoryList.as_view(), name="admin-categories"),
    path("categories/create/", CategoryCreate.as_view(), name="admin-categories-create"),
    path("categories/detail/<str:pk>/", CategoryDetail.as_view(), name="admin-categories-detail"),
    path("categories/edit/<str:pk>/", CategoryEdit.as_view(), name="admin-categories-edit"),
    path("categories/delete/<str:pk>/", CategoryDelete.as_view(), name="admin-categories-delete"),
    # Product
    path("products/", ProductsList.as_view(), name="admin-products"),
    path("products/create/", ProductsCreate.as_view(), name="admin-products-create"),
    path("products/detail/<str:pk>/", ProductsDetail.as_view(), name="admin-products-detail"),
    path("products/edit/<str:pk>/", ProductsEdit.as_view(), name="admin-products-edit"),
    path("products/delete/<str:pk>/", ProductsDelete.as_view(), name="admin-products-delete"),
    # Dynamic Pages
    path("pages/", DynamicPagesList.as_view(), name="admin-pages"),
    path("pages/create/", DynamicPagesCreate.as_view(), name="admin-pages-create"),
    path("pages/detail/<str:pk>/", DynamicPagesDetail.as_view(), name="admin-pages-detail"),
    path("pages/edit/<str:pk>/", DynamicPagesEdit.as_view(), name="admin-pages-edit"),
    path("pages/delete/<str:pk>/", DynamicPagesDelete.as_view(), name="admin-pages-delete"),

]