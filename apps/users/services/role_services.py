from ..models import Role

class RoleService:
    @staticmethod
    def create_role(tenant, name, description, is_active, permissions=[]):
        role = Role.objects.create(
            tenant=tenant,
            name=name,
            description=description,
            is_active=is_active
        )
        role.permissions.set(permissions)
        return role
    
    @staticmethod
    def update_role(role, name=None, description=None, is_active = None, permissions=None):
        if name:
            role.name = name
            
        if description:
            role.description = description
            
        if is_active:
            role.is_active = is_active
            
        role.save()
        if permissions is not None:
            role.permissions.set(permissions)
        return role