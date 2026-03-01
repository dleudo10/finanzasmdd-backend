from django.db import models
from apps.core.models import TimesTampTime
from simple_history.models import HistoricalRecords
from .list_price import ListPrice
from .product import Product
from django.core.exceptions import ValidationError

class PriceSalesHistory(TimesTampTime):
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name="price_sales_history"
    )
    list_price = models.ForeignKey(
        ListPrice,
        on_delete=models.PROTECT
    )
    unit_costo = models.DecimalField('costo unitario', max_digits=10, decimal_places=2)
    date_start = models.DateField('fecha de inicio')
    date_end = models.DateField('fecha de finalización', null=True, blank=True)
    
    def clean(self):
        if self.unit_costo <= 0:
            raise ValidationError({"unit_costo": "El costo unitario debe ser mayor a 0."})
    
        if self.date_end and self.date_end < self.date_start:
            raise ValidationError({"date_end": "La fecha de finalización no puede ser menor a la fecha de inicio."})
    
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.product} ${self.unit_costo}"
    
    class Meta:
        db_table = "price_sales_history"
        verbose_name = "historial de precio de venta"
        verbose_name_plural = "historial de precios de venta"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "list_price", "date_start"],
                name="unique_product_listprice_date_start"
            ),
        ]