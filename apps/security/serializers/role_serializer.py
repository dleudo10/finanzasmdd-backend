from rest_framework import serializers
from ..models import Role, Permission
from ..services.role_services import RoleService

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all()
    )
    
    class Meta:
        model = Role
        fields = ['name', 'description', 'permissions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        tenant = self.context['request'].tenant
        return RoleService.create_role(tenant=tenant, **validated_data, permissions=permissions)
    
    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        return RoleService.update_role(role=instance, **validated_data, permissions=permissions) 
        
        