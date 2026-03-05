from apps.core.views import BaseStateViewSet
from ..models import Warehouse
from ..serializers import WarehouseSerializer

class WarehouseViewSet(BaseStateViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_map = {
        "list": "warehouse.view",
        "retrieve": "warehouse.view",
        "create": "warehouse.create",
        "update": "warehouse.update",
        "partial_update": "warehouse.update",
        "destroy": "warehouse.delete",
    }
    search_fields = ['name', 'location']
    
    def get_queryset(self):
        tenant = self.request.tenant
        return Warehouse.objects.filter(tenant=tenant)