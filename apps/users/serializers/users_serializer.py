from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Role, TenantUser
from ..services.users_services import UsersService
User = get_user_model()

class UsersSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all()
    ) 
    
    class Meta:
        model = User
        fields = [
            'name', 
            'lastname', 
            'document_type', 
            'document_number', 
            'phone', 
            'email', 
            'is_staff', 
            'is_active',
            'role'
        ]
        read_only_fields = ['document_type', 'document_number', 'role']
        
    def validate_role(self, role):
        tenant = self.context["request"].tenant
        if role.tenant_id != tenant.id:
            raise serializers.ValidationError("El rol no pertenece al tenant")
        return role
    
    def create(self, validated_data):
        request = self.context["request"]
        tenant = request.tenant
        
        return UsersService.create_user(
            tenant=tenant,
            **validated_data
        )
        
    def update(self, instance, validated_data):
        tenant = self.context["request"].tenant
        tenant_user = TenantUser.objects.filter(user=instance, tenant=tenant).first()
        
        return UsersService.update_user(
            user=instance,
            tenant_user=tenant_user,
            **validated_data
        )
        
class UserChangeRoleSerializer(serializers.Serializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all()
    )
    
    def validate_role(self, role):
        tenant_user = self.context["tenant_user"]
        if role.tenant_id != tenant_user.tenant_id:
            raise serializers.ValidationError("Rol no pertenece al tenant")
        return role
    
    def save(self):
        tenant_user = self.context["tenant_user"]
        new_role = self.validated_data["role"]

        return UsersService.change_role(
            tenant_user=tenant_user,
            new_role=new_role
        )