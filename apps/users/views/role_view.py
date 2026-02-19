from rest_framework import viewsets
from ..models import Role
from ..serializers import RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    
    def get_queryset(self):
        tenant = self.request.tenant
        return Role.objects.filter(tenant=tenant, is_owner_role=False, is_active=True)