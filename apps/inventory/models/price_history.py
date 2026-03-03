from django.db import models
from apps.core.models import TimesTampTime
from simple_history.models import HistoricalRecords
from .list_price import ListPrice
from .product_unit import ProductUnit
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from ..choices import TypePriceChoices
from apps.users.models import Tenant
from django.utils import timezone


class PriceHistory(TimesTampTime):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT
    )
    product_unit = models.ForeignKey(
        ProductUnit, 
        on_delete=models.PROTECT, 
        related_name="price_history"
    )
    list_price = models.ForeignKey(
        ListPrice,
        on_delete=models.PROTECT
    )
    type_price = models.CharField('tipo de precio', max_length=8, choices=TypePriceChoices.choices)
    price = models.DecimalField('precio', max_digits=10, decimal_places=2)
    date_start = models.DateField('fecha de inicio', default=timezone.now)
    reason_change = models.TextField(
        'motivo de cambio', 
        null=True, 
        blank=True, 
        validators=[MinLengthValidator(10, "Debe tener al menos 10 caracteres.")]
    )
    date_end = models.DateField('fecha de finalización', null=True, blank=True)
    
    
    def clean(self):
        if self.tenant_id != self.product_unit.tenant_id:
            raise ValidationError({"product": "El producto no existe dentro de esta empresa"}) 
        
        if self.tenant_id != self.list_price.tenant_id:
            raise ValidationError({"list_price": "La lista de precio no existe dentro de esta empresa"})
        
        if self.price <= 0:
            raise ValidationError({"price": "El price debe ser mayor a 0."})
    
        if self.date_end and self.date_end < self.date_start:
            raise ValidationError({"date_end": "La fecha de finalización no puede ser menor a la fecha de inicio."})
    
    history = HistoricalRecords()
    
    def _validate_immutable_fields(self, orig):
        blocked_fields = ['tenant_id', 'product_unit_id', 'list_price_id', 'type_price', 'price', 'date_start']
        for field in blocked_fields:
            if getattr(self, field) != getattr(orig, field):
                raise ValidationError(f"No se puede editar el campo '{field}' de un registro histórico")
        
        if orig.date_end is not None:
            if  self.tenant_id != orig.tenant_id or self.reason_change != orig.reason_change or self.date_end != orig.date_end:
                raise ValidationError("No se puede editar un registro que ya tiene fecha de finalización")

    
    def save(self, *args, **kwargs):
        if self.pk:
            orig = type(self).objects.get(pk=self.pk)
            self._validate_immutable_fields(orig)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_unit} ${self.price}"
    
    class Meta:
        db_table = "price_sales_history"
        verbose_name = "historial de precio de venta"
        verbose_name_plural = "historial de precios de venta"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "product_unit", "list_price"],
                name="unique_price_per_tenant_product_list"
            ),
            models.UniqueConstraint(
                fields=['product_unit', 'list_price', 'type_price'],
                condition=models.Q(date_end__isnull=True),
                name='unique_active_price_per_product_list_type'
            )
        ]
        indexes = [
            models.Index(fields=["tenant", "date_start"]),
            models.Index(fields=["tenant", "date_end"]),
            models.Index(fields=["tenant", "product_unit", "list_price"])
        ]