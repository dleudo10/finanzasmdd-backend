from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Permite el acceso solo al propietario del objeto"""
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user
    
class IsTenantOwner(BasePermission):
    """Permite saber quien es el dueño del tenant"""
    
    message = "No tienes permisos para acceder a este tenant"
    
    def has_object_permission(self, request, view, obj):
        tenant = getattr(request, "tenant", None)
        
        if tenant is None:
            return False
        
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        
        return tenant.owner == request.user