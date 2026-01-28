from rest_framework import serializers

from products.models import Products
from users.models import User

class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)   
    
    # read only field in serializer
    category_response = serializers.SerializerMethodField() 

    def get_category_response(self, obj):
        return CategorySerializer(instance=obj.category).data

    class Meta:
        model = Products
        fields="__all__"


class UserMSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "role"]

class UserSerializer(serializers.Serializer):
    email = serializers.CharField()
    role = serializers.CharField()
