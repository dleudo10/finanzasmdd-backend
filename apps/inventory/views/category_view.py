from apps.core.views import BaseStateViewSet
from ..models import Category
from ..serializers import CategorySerializer

class CategoryViewSet(BaseStateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        tenant = self.request.tenant
        return Category.objects.filter(tenant=tenant) 