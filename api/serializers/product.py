from rest_framework import serializers

from products.models import Products
from users.models import User

class ProductSerializer(serializers.ModelSerializer):
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