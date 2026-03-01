from django.db import models
from apps.users.models import Tenant
from simple_history.models import HistoricalRecords
from apps.inventory.models import Product, Warehouse
from .choices import TypeMovementsChoices
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class Movement(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="kardex"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="movements"
    )
    type = models.CharField('tipo de movimiento', max_length=10, choices=TypeMovementsChoices.choices)
    quantity = models.PositiveIntegerField('cantidad')
    unit_cost = models.DecimalField('costo unitario', max_digits=10, decimal_places=2)
    date = models.DateTimeField('fecha', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    @property
    def total(self):
        return self.quantity * self.unit_cost
    
    history = HistoricalRecords()
    
    def clean_unit_cost(self):
        if self.unit_cost <= 0:
            raise ValidationError("El costo unitario debe de ser mayor a 0.")
        
    def clean_quantity(self):
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe de ser mayor a 0.")
    
    def __str__(self):
        return f"{self.product} - {self.warehouse} Cantidad {self.quantity} Total ${self.total}"
    
    class Meta:
        db_table = "movements"
        verbose_name = "movimiento"
        verbose_name_plural = "movimientos"
    
    
    
# from django.contrib.contenttypes.models import ContentType

# sale = Sale.objects.first()
# movement = Movement.objects.create(
#     content_type=ContentType.objects.get_for_model(Sale),
#     object_id=sale.id,
#     quantity=-5
# )

# print(movement.content_object)