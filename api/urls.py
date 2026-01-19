from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.viewsets.categories import CategoryViewset
from api.viewsets.product import ProductViewset

router = DefaultRouter()
router.register("products", ProductViewset, basename="Products")
router.register("categories", CategoryViewset, basename="Categories")

urlpatterns = [
    path("", include(router.urls)),
]