from rest_framework import serializers
from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def create(self, validated_data):
        tenant = self.context["request"].tenant
        return Category.objects.create(
            tenant=tenant,
            **validated_data
        )