from django.test import TestCase
from ..models import Plan
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class PlanTest(TestCase):
    
    def setUp(self):
        """Preparación de datos base que no cambian entre tests"""
        self.valid_data = {
            "name" : "Plan Pro",
            "price" : 99.99,
            "user_limit" : 10
        }
        
        return super().setUp()
    
    ## --- HAPPY PATH (Camino Exitoso) ---
    def test_create_plan_successfully(self):
        """Verifica que el plan cree toda la estructura correctamente"""

        plan = Plan.objects.create(**self.valid_data)
        
        self.assertEqual(plan.name, "Plan Pro")
        self.assertEqual(plan.price, 99.99)
        self.assertEqual(plan.user_limit, 10)
        
    def test_price_cannot_be_negative(self):
        """Validar que el validador de precio mínimo funcione"""
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = -99.99
        plan = Plan(**invalid_data)
        
        with self.assertRaises(ValidationError):
            plan.full_clean()
            
    def test_unique_name_constraint(self):
        """La base de datos debe impedir nombres duplicados"""
        Plan.objects.create(name="Basic", price=10, user_limit=1)
        with self.assertRaises(IntegrityError):
            Plan.objects.create(name="Basic", price=20, user_limit=5)
            
    
    def test_unique_name_constraint(self):
        """La base de datos debe impedir nombres duplicados"""
        Plan.objects.create(name="Basic", price=10, user_limit=1)
        with self.assertRaises(IntegrityError):
            Plan.objects.create(name="Basic", price=20, user_limit=5)