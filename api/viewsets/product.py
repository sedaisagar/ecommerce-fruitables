from rest_framework import viewsets

from api.serializers.product import ProductSerializer
from products.models import Products

from drf_spectacular.utils import extend_schema

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

@extend_schema(tags=["Product(s)"])
class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [ BasicAuthentication]