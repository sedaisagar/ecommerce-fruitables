from rest_framework import viewsets,generics

from api.serializers.product import ProductSerializer, UserMSerializer, UserSerializer
from products.models import Products

from drf_spectacular.utils import extend_schema

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

from users.models import User

@extend_schema(tags=["Product(s)"])
class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    # filterset_fields = ['name']
    # authentication_classes = [ BasicAuthentication]

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



@extend_schema(tags=["Public Api(s)"])
class PublicProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


from rest_framework.views import APIView
from rest_framework.response import Response
@extend_schema(tags=["Public Api(s)"])
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        queryset = User.objects.all()
        
        # serializer = UserMSerializer(queryset, many=True)
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data = request.data)
        if valid:=serializer.is_valid():
            serializer.save()
        
        return Response(serializer.data if valid else serializer.errors, status=200 if valid else 400)
