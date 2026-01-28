from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.viewsets.categories import CategoryViewset
from api.viewsets.product import ProductViewset , PublicProductView, ListUsers

router = DefaultRouter()
router.register("products", ProductViewset, basename="Products")
router.register("categories", CategoryViewset, basename="Categories")
# router.register("public-product", PublicProductView, basename="PPV")


urlpatterns = [
    path("", include(router.urls)),
    path("public-products/<str:id>/", PublicProductView.as_view()),
    path("users/", ListUsers.as_view())
]