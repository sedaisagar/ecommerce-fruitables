from rest_framework import serializers

from products.models import Category, Products

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug"]

class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)   
    
    # read only field in serializer
    category_response = serializers.SerializerMethodField() 

    def get_category_response(self, obj):
        return CategorySerializer(instance=obj.category).data

    class Meta:
        model = Products
        fields = "__all__"

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        # data["category"] = CategorySerializer(instance=instance.category).data
        return data
      
      