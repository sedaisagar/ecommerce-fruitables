from rest_framework import viewsets

from api.serializers.product import ProductSerializer
from products.models import Products #, generics,mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all() 
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]