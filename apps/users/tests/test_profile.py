from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.users.models import Tenant, Plan
from apps.core.choices import TypeDocument, TypePerson
User = get_user_model()

class ProfileAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email = "test@ejemplo.com",
            password = "Password123*",
            name = "Jon",
            lastname = "Doe"
        )
        
        self.tenant = Tenant(
            owner=self.user,
            trade_name="Empresa XYZ",
            type_person=TypePerson.LEGAL,
            document_type=TypeDocument.NIT,
            document_number="900123456-1",
            phone="3001234567"
        )
        
        self.plan = Plan.objects.create(
            name="Plan Pro",
            price=99.99,
            user_limit=10
        )
        
        self.client.force_authenticate(user=self.user)
        
    def test_no_header(self):
        """Si no se envia X-Tenant, devuelve 400"""
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, 400)
        
    def test_invalid_tenant(self):
        """Si se envía X-Tenant que no existe, devuelve 404"""
        response = self.client.get("/api/me/", HTTP_X_TENANT="empresa_falsa")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Tenant inválido", response.data["message"])
        
    def test_valid_tenant(self):
        """Si se envía X-Tenant válido, permite acceso"""
        response = self.client.get("/fake-url/", HTTP_X_TENANT=self.tenant.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["tenant"], self.tenant.trade_name)