from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import TenantUser
User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['name', 'lastname', 'document_type', 'document_number', 'phone', 'email', 'created_at', 'updated_at', 'role', 'permissions']
        read_only_fields = ['document_type', 'document_number', 'email', 'created_at', 'updated_at', 'role', 'permissions']
    
    def _get_tenant_user(self, obj):
        if not hasattr(self, "_tenant_user"):
            self._tenant_user = TenantUser.objects.select_related(
                "role"
            ).prefetch_related(
                "role__permissions"
            ).filter(
                user=obj,
                tenant=self.context["tenant"]
            ).first()
        return self._tenant_user
    
    def get_role(self, obj):
        tenant_user = self._get_tenant_user(obj)
        return tenant_user.role.name if tenant_user else None
    
    def get_permissions(self, obj):        
        tenant_user = self._get_tenant_user(obj)
        
        if not tenant_user:
            return []
        
        return list(
            tenant_user.role.permissions.values_list("description", flat=True)
        )