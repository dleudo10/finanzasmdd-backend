from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from datetime import timedelta
from apps.core.choices import SubscriptionStatus, TypePerson, TypeDocument

from ..models import User, Tenant, Role, TenantUser, Plan, Subscription, Permission
from ..services.tenant.create_tenant import CreateTenantService

class CreateTenantServiceTest(TestCase):
    
    def setUp(self):
        """Preparación de datos base que no cambian entre tests"""
        self.plan = Plan.objects.create(
            name="Plan Pro",
            price=99.99,
            user_limit=10
        )
        # Creamos algunos permisos para verificar la asignación al rol ADMIN
        self.perm1 = Permission.objects.create(code="view_dashboard", description="Ver dashboard")
        self.perm2 = Permission.objects.create(code="edit_users", description="Editar usuarios")

        self.valid_data = {
            "trade_name": "Tech Solutions SAS",
            "document_type": TypeDocument.NIT, 
            "document_number": "900123456-1",
            "type_person": TypePerson.LEGAL,
            "phone": "3001234567",
            "email": "owner@techsolutions.com",
            "name": "John",
            "lastname": "Doe",
            "owner_password": "secure_password_123",
            "plan": self.plan,
            "plan_status": SubscriptionStatus.ACTIVE,
            "observations": "Primer registro de cliente"
        }

    ## --- HAPPY PATH (Camino Exitoso) ---

    def test_execute_creates_all_objects_successfully(self):
        """Verifica que el servicio cree toda la estructura relacional correctamente"""
        tenant = CreateTenantService.execute(**self.valid_data)

        # Verificar Tenant
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(tenant.trade_name, "Tech Solutions SAS")
        self.assertEqual(tenant.owner.email, "owner@techsolutions.com")

        # Verificar Usuario y Password Hasheada
        user = User.objects.get(email="owner@techsolutions.com")
        self.assertTrue(user.check_password("secure_password_123"))

        # Verificar Suscripción y Fechas
        subscription = Subscription.objects.get(tenant=tenant)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.status, SubscriptionStatus.ACTIVE)
        self.assertIsNotNone(subscription.end_date)
        # Verificar que la fecha final sea aprox 30 días después de la inicial
        expected_end = subscription.start_date + timedelta(days=30)
        self.assertEqual(subscription.end_date, expected_end)

        # Verificar Roles y Permisos
        role = Role.objects.get(tenant=tenant, name="ADMIN")
        self.assertEqual(role.permission.count(), 2)
        self.assertIn(self.perm1, role.permission.all())

        # Verificar Vinculación (TenantUser)
        self.assertTrue(TenantUser.objects.filter(user=user, tenant=tenant, role=role).exists())

    ## --- EDGE CASES & NEGATIVE TESTS (Casos de Borde y Errores) ---
    def test_reuse_existing_user(self):
        """Verifica que si el usuario ya existe, se use el mismo y no falle"""
        existing_user = User.objects.create(
            email="owner@techsolutions.com",
            name="Existing",
            lastname="User"
        )
        
        tenant = CreateTenantService.execute(**self.valid_data)
        
        self.assertEqual(tenant.owner.id, existing_user.id)
        self.assertEqual(User.objects.count(), 1)

    def test_transaction_rollback_on_failure(self):
        """
        Verifica que si la creación de la suscripción falla, 
        no se cree ni el Tenant ni el Usuario (Atomicidad)
        """
        invalid_data = self.valid_data.copy()
        invalid_data['plan'] = None

        with self.assertRaises(ValidationError):
            CreateTenantService.execute(**invalid_data)

        self.assertEqual(Tenant.objects.count(), 0)
        self.assertEqual(User.objects.filter(email="owner@techsolutions.com").count(), 0)

    def test_duplicate_tenant_document_fails(self):
        """Verifica que la restricción de documento único en Tenant funcione"""
        CreateTenantService.execute(**self.valid_data)
        
        # Intentamos crear otro con el mismo número de documento
        duplicate_data = self.valid_data.copy()
        duplicate_data['email'] = "other@email.com"
        
        with self.assertRaises(IntegrityError):
            CreateTenantService.execute(**duplicate_data)

    def test_subscription_pending_status_no_end_date(self):
        """Verifica que si el status no es ACTIVE, no se asigne end_date automáticamente"""
        data = self.valid_data.copy()
        data['plan_status'] = SubscriptionStatus.PENDING
        
        tenant = CreateTenantService.execute(**data)
        subscription = Subscription.objects.get(tenant=tenant)
        
        self.assertIsNone(subscription.end_date) 
        
        