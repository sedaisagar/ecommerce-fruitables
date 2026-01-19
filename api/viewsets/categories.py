from rest_framework import viewsets

from api.serializers.categories import CategorySerializer
from products.models import Category

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Category(s)"])
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
