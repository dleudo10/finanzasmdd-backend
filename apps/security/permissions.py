from rest_framework.permissions import BasePermission
from apps.users.models import TenantUser

class HasPermission(BasePermission):
    def has_permission(self, request, view):
        permission_map = getattr(view, "permission_map", None)
        action = getattr(view, "action", request.method.lower())
        tenant = getattr(request, "tenant", None)

        if not all([permission_map, action, tenant]):
            return False
        
        # if TenantUser.objects.filter(
        #     user=request.user,
        #     tenant=tenant,
        #     role__is_owner_role=True
        # ).exists():
        #     return True
        
        required_permission = permission_map.get(action)
        if not required_permission:
            return False

        return TenantUser.objects.filter(
            user=request.user,
            tenant=tenant,
            role__permissions__code=required_permission
        ).exists()