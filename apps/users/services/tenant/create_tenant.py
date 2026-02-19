from django.db import transaction
from ...models import Tenant, Role, TenantUser, Permission, Plan, Subscription
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from apps.core.choices import SubscriptionStatus

User = get_user_model()

class CreateTenantService:
    @staticmethod
    @transaction.atomic
    def execute(*, 
                trade_name: str, 
                document_type: str, 
                document_number: str, 
                type_person: str, 
                phone: str, 
                email: str, 
                name: str, 
                lastname: str, 
                owner_password: str,
                plan: Plan,
                plan_status: str,  
                observations: str = None,
    ) -> Tenant:
        
        # Creación de usuarip
        user, created = User.objects.get_or_create(
            email=email.lower(),
            defaults={
                "name": name,
                "lastname": lastname,
                "document_type": document_type,
                "document_number": document_number, 
                "phone": phone
            }
        )
        
        if created:
            user.set_password(owner_password)
            user.save()

        # Creación del Tenant
        tenant = Tenant.objects.create(
            owner=user,
            trade_name=trade_name,
            type_person=type_person,
            document_type=document_type,
            document_number=document_number,
            phone=phone
        )

        # asignación de suscripcion inicial
        suscripcion = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status=plan_status,
            observations=observations,
            start_date=timezone.now(),
        )

        if suscripcion.status == SubscriptionStatus.ACTIVE:
            suscripcion.end_date = suscripcion.start_date + timedelta(days=30)
        
        suscripcion.save()

 
        # Configuración de Roles y Permisos
        admin_role, _ = Role.objects.get_or_create(
            tenant=tenant,
            name="DUEÑO",
            defaults={"description": "Acceso total al sistema"},
            is_owner_role = True
        )
        
        all_permissions = Permission.objects.all()
        admin_role.permissions.set(all_permissions)

        # Vinculación Usuario-Tenant
        TenantUser.objects.create(
            user=user,
            tenant=tenant,
            role=admin_role
        )

        return tenant