from django.db import models
from apps.core.models import BaseState, TimesTampTime
from .category import Category
from simple_history.models import HistoricalRecords
from apps.users.models import Tenant

class Product(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField('nombre', max_length=200)
    description = models.TextField('descripcion', null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="products"
    )
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "products"
        verbose_name = "producto"
        verbose_name_plural = "productos"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_product_name_tenant"
            )
        ]
    
    