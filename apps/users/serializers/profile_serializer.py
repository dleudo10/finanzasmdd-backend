from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from ..models import TenantUser
User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    document_type = serializers.CharField(
        source='get_document_type_display'
    )
    
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField() 
    
    class Meta:
        model = User
        fields = ['name', 'lastname', 'document_type', 'document_number', 'phone', 'email', 'role', 'permissions']
        read_only_fields = ['email', 'document_type', 'document_number', 'role', 'permissions']
    
    def _get_tenant_user(self, obj):
        if not hasattr(self, "_tenant_user"):
            self._tenant_user = TenantUser.objects.select_related(
                "role"
            ).prefetch_related(
                "role__permissions"
            ).filter(
                user=obj,
                tenant = self.context["request"].tenant
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


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")

        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "La contraseñas no coinciden."}
            )

        password_validation.validate_password(
            attrs['new_password'],
            self.context['request'].user
        )

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user