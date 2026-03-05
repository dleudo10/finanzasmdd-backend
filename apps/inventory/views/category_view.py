from apps.core.views import BaseStateViewSet
from ..models import Category
from ..serializers import CategorySerializer

class CategoryViewSet(BaseStateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name', 'description']
    permission_map = {
        "list": "category.view",
        "retrieve": "category.view",
        "create": "category.create",
        "update": "category.update",
        "partial_update": "category.update",
        "destroy": "category.delete",
    }
    
    def get_queryset(self):
        tenant = self.request.tenant
        return Category.objects.filter(tenant=tenant) 