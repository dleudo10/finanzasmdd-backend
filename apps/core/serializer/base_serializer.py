from rest_framework import serializers

class TenantModelSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        tenant = self.context["request"].tenant
        validated_data["tenant"] = tenant
        return super().create(validated_data)