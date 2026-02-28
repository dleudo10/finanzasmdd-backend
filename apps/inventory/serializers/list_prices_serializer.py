from ..models import ListPrice
from apps.core.serializer import TenantModelSerializer

class ListPriceSerializer(TenantModelSerializer):
    class Meta:
        model = ListPrice
        fields = ['id', 'name', 'is_main', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    