from django.db import models
from apps.core.models import TimesTampTime
from .product import Product
from .warehouse import Warehouse
from simple_history.models import HistoricalRecords

class Stock(TimesTampTime):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stocks"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stocks"
    )
    quantity = models.PositiveIntegerField('cantidad')
    average_cost = models.DecimalField('costo promedio', max_digits=10, decimal_places=2)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.product} bodega: {self.warehouse} cantidad: {self.quantity}"
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        
    # Restricciones:
    #Un producto por bodega
    # indices de productos y warehouse