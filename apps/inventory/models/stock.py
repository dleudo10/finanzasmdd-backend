from django.db import models
from apps.core.models import TimesTampTime
from .product_unit import ProductUnit
from .warehouse import Warehouse
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from apps.users.models import Tenant

class Stock(TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    product_unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.PROTECT,
        related_name="stocks"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stocks"
    )
    quantity = models.PositiveIntegerField('cantidad')
    average_cost = models.DecimalField('costo promedio', max_digits=10, decimal_places=2)
    
    history = HistoricalRecords()
    
    def clean(self):
        if not self.product_unit.is_base:
            raise ValidationError({"product": "El producto no contiene la unidad base"})
        
        if self.tenant_id != self.product_unit.tenant_id:
            raise ValidationError({"product": "El producto no existe dentro de esta empresa"})  
        
        if self.tenant_id != self.warehouse.tenant_id:
            raise ValidationError({"warehouse": "La bodega no existe dentro de esta empresa"}) 
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)  
    
    def __str__(self):
        return f"{self.product_unit} bodega: {self.warehouse} cantidad: {self.quantity}"
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "product_unit", "warehouse"],
                name="unique_stock_tenant_product_unit_warehouse"
            ),
        ]
        indexes = [
            models.Index(fields=["tenant", "product_unit", "warehouse"]),     
        ]