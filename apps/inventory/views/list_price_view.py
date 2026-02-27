from apps.core.views import BaseStateViewSet
from ..models import ListPrice
from ..serializers import ListPriceSerializer

class ListPriceViewSet(BaseStateViewSet):
    queryset = ListPrice.objects.all()
    serializer_class = ListPriceSerializer
    search_fields = ['name']
    
    def get_queryset(self):
        tenant = self.request.tenant
        return ListPrice.objects.filter(tenant=tenant)