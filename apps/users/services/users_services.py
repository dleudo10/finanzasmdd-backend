from django.db import transaction
from ..models import TenantUser, Tenant, Role
from django.contrib.auth import get_user_model
User = get_user_model()

class UsersService:
    @staticmethod
    @transaction.atomic
    def create_user(*,
                    name: str,
                    lastname: str,
                    document_type: str,
                    document_number: str,
                    phone: str,
                    email: str,
                    password: str,
                    is_staff: bool,
                    is_active: bool,
                    tenant: Tenant,
                    role: Role,
    ) -> User:
        
        if role.tenant_id != tenant.id:
            raise ValueError("Rol no pertenece al tenant")
        
        if User.objects.filter(email=email.lower()).exists():
            raise ValueError("El usuario con este correo electrónico ya existe")
        
        user = User.objects.create(
            email=email.lower(),
            name=name,
            lastname=lastname,
            document_type=document_type,
            document_number=document_number,
            phone=phone,
            is_staff=is_staff,
            is_active=is_active
        )
        
        user.set_password(password)
        user.save()
            
        TenantUser.objects.create(
            user=user,
            tenant=tenant,
            role=role
        )
            
        return user
    
    @staticmethod
    @transaction.atomic
    def update_user(*,
                    user: User,
                    tenant_user: TenantUser,
                    name: str | None = None,
                    lastname: str | None = None,
                    phone: str | None = None,
                    email: str | None = None,
                    role: Role | None = None,
    ):
        if name:
            user.name = name
            
        if lastname:
            user.lastname = lastname
            
        if phone:
            user.phone = phone
            
        if email:
            user.email = email
            
        if role:
            if role.tenant_id != tenant_user.tenant_id:
                raise ValueError("Rol no pertenece al tenant")
            tenant_user.role = role
            
        user.save()
        tenant_user.save()
        return user
    
    @staticmethod
    @transaction.atomic
    def change_role(*,
                    tenant_user: TenantUser,
                    new_role: Role,
    ) -> TenantUser:

        if new_role.tenant_id != tenant_user.tenant_id:
            raise ValueError("Rol no pertenece al tenant")

        tenant_user.role = new_role
        tenant_user.save()

        return tenant_user
    
    @staticmethod
    @transaction.atomic
    def deactivate_user(*,
                        user: User,
    ) -> User:

        if not user.is_active:
            return user  

        user.is_active = False
        user.save(update_fields=["is_active"])

        return user
            
        