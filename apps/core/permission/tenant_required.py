from rest_framework.permissions import BasePermission

class TenantRequired(BasePermission):
    message = "Tenant requerido o invalido"
    
    def has_permission(self, request, view):
        return request.tenant is not None