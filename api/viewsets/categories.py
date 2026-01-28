from rest_framework import viewsets, mixins

from api.serializers.categories import CategorySerializer, MyActionSerializer
from products.models import Category

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

from utils.custom_permissions import IsCustomer, IsSystemAdmin

@extend_schema(tags=["Category(s)"])
class CategoryViewset(mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['name']
    # http_method_names = [
    #     # 'get',
    #     'put',
    #     'delete',
    # ]

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSystemAdmin]

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True)

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'my_action':
            return MyActionSerializer
        
        return super().get_serializer_class()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)

    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        # Serializer works on single as well as multiple objects
        # CategorySerializer(self.filter_queryset(self.get_queryset()), many=True)

        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['patch'],url_path='other-action')
    def my_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data_ok = serializer.is_valid(raise_exception=False)
        if not data_ok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"This is other action", "submitted_data":request.data}, status=status.HTTP_200_OK)