from ..models import Warehouse
from apps.core.serializer import TenantModelSerializer

class WarehouseSerializer(TenantModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location',  'observations', 'is_main', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    