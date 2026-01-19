from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.viewsets.product import ProductViewSet


# Router instance
router = DefaultRouter()
router.register('products', ProductViewSet, basename='ecom-products')


urlpatterns = [
    path("", include(router.urls)),
]