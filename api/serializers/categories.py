from rest_framework import serializers

from products.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields=['id', 'name', 'slug', 'created_at', 'updated_at']
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cats = instance.children.all()
        if cats.exists():
            data["categories"] = CategorySerializer(cats, many=True).data
        return data
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    