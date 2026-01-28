from rest_framework import serializers

from api.serializers.categories import CategorySerializer
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
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLES)

    def create(self, validated_data):
        return validated_data
    
    def update(self, instance, validated_data):
        
        for k ,v in validated_data.items():
            setattr(instance, k , v)

        instance.save() 

        return validated_data
    
    def to_representation(self, instance:dict):
        if isinstance(instance, dict):
            return {"message": f"User {instance["email"]} with role {instance["role"]} created successfully."}
        else:
            return super().to_representation(instance)