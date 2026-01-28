from rest_framework import viewsets

from api.serializers.product import ProductSerializer
from products.models import Products

from drf_spectacular.utils import extend_schema

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=["Product(s)"])
class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]

    # filterset_fields = ['name']
    # authentication_classes = [ BasicAuthentication]
