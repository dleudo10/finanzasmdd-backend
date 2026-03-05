from apps.core.views import BaseStateViewSet
from ..models import ListPrice
from ..serializers import ListPriceSerializer

class ListPriceViewSet(BaseStateViewSet):
    queryset = ListPrice.objects.all()
    serializer_class = ListPriceSerializer
    search_fields = ['name']
    permission_map = {
        "list": "list_price.view",
        "retrieve": "list_price.view",
        "create": "list_price.create",
        "update": "list_price.update",
        "partial_update": "list_price.update",
        "destroy": "list_price.delete",
    }
    
    def get_queryset(self):
        tenant = self.request.tenant
        return ListPrice.objects.filter(tenant=tenant)