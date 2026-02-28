from apps.core.views import BaseStateViewSet
from ..models import Warehouse
from ..serializers import WarehouseSerializer

class WarehouseViewSet(BaseStateViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    search_fields = ['name', 'location']
    
    def get_queryset(self):
        tenant = self.request.tenant
        return Warehouse.objects.filter(tenant=tenant)