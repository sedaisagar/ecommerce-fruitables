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
    

class MyActionSerializer(serializers.Serializer):
    ACTIONS = (
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
    )
    action = serializers.ChoiceField(choices=ACTIONS)
    reason = serializers.CharField(required=False, allow_blank=True, max_length=200)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=10)
    