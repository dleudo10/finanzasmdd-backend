from apps.core.serializer import TenantModelSerializer
from ..models import Category

class CategorySerializer(TenantModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    