from rest_framework import serializers
from ..models import Tenant

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['trade_name', 'type_person', 'document_type', 'document_number', 'phone', 'adress', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['type_person', 'document_type', 'document_number', 'is_active', 'created_at', 'updated_at']