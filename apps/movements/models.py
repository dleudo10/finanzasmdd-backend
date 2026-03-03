from django.db import models
from apps.users.models import Tenant
from simple_history.models import HistoricalRecords
from apps.inventory.models import ProductUnit, Warehouse
from .choices import TypeMovementsChoices, TypeNaturalityChoices
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Movement(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    product_unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.PROTECT,
        related_name="kardex"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="movements"
    )
    type = models.CharField('tipo de movimiento', max_length=15, choices=TypeMovementsChoices.choices)
    naturality = models.CharField('naturaleza', max_length=5, choices=TypeNaturalityChoices.choices)
    quantity = models.PositiveIntegerField('cantidad')
    unit_cost = models.DecimalField(
        'costo unitario', 
        max_digits=10, 
        decimal_places=2
    )
    date = models.DateTimeField('fecha', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    observations = models.TextField(
        "observaciones", 
        null=True, 
        blank=True,         
        validators=[MinLengthValidator(10, "Debe tener al menos 10 caracteres.")]
    )
    
    @property
    def total(self):
        return self.quantity * self.unit_cost
    
    history = HistoricalRecords()
    
    VALID_TYPE_NATURALITY = {
        TypeMovementsChoices.INITIAL: TypeNaturalityChoices.ENTRY,

        TypeMovementsChoices.PURCHASE: TypeNaturalityChoices.ENTRY,
        TypeMovementsChoices.PURCHASE_RETURN: TypeNaturalityChoices.EXIT,

        TypeMovementsChoices.SALE: TypeNaturalityChoices.EXIT,
        TypeMovementsChoices.SALE_RETURN: TypeNaturalityChoices.ENTRY,

        TypeMovementsChoices.ADJUSTMENT_IN: TypeNaturalityChoices.ENTRY,
        TypeMovementsChoices.ADJUSTMENT_OUT: TypeNaturalityChoices.EXIT,

        TypeMovementsChoices.TRANSFER_IN: TypeNaturalityChoices.ENTRY,
        TypeMovementsChoices.TRANSFER_OUT: TypeNaturalityChoices.EXIT,
    }
        
    def clean(self):
        if self.pk:
            original = type(self).objects.only("tenant_id").get(pk=self.pk)

            if original.tenant_id != self.tenant_id:
                raise ValidationError({
                    "tenant": "No se puede cambiar el tenant de una bodega existente."
                })
                
        if self.unit_cost <= 0:
            raise ValidationError({"unit_cost": "El costo unitario debe de ser mayor a 0."})
        
        if self.quantity <= 0:
            raise ValidationError({"quantity": "La cantidad debe ser mayor a 0."})
        
        if self.tenant_id != self.product_unit.tenant_id:
            raise ValidationError({"product": "El producto no existe dentro de esta empresa"}) 
        
        if self.tenant_id != self.warehouse.tenant_id:
            raise ValidationError({"warehouse": "La bodega no existe dentro de esta empresa"})  
    
        if not self.warehouse.is_active:
            raise ValidationError({"warehouse": "No se puede crear stock en una bodega inactiva"})        

        if not self.product_unit.is_active:
            raise ValidationError({"product": "No se puede registrar movimientos para un producto inactivo"})
        
        if self.content_object and hasattr(self.content_object, "tenant_id"):
            if self.content_object.tenant_id != self.tenant_id:
                raise ValidationError("El documento relacionado no pertenece a este tenant.")
        
        expected_naturality = self.VALID_TYPE_NATURALITY.get(self.type)

        if expected_naturality and self.naturality != expected_naturality:
            raise ValidationError({
                "naturality": (
                    f"La naturaleza '{self.naturality}' "
                    f"no es válida para el tipo '{self.type}'."
                )
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product_unit} - {self.warehouse} Cantidad {self.quantity} Total ${self.total}"    
    
    class Meta:
        db_table = "movements"
        verbose_name = "movimiento"
        verbose_name_plural = "movimientos"
        indexes = [
            models.Index(fields=["product_unit", "warehouse"]),
            models.Index(fields=["tenant", "date"]),
            models.Index(fields=["tenant", "product_unit", "warehouse"])
        ]
    
    
    
# from django.contrib.contenttypes.models import ContentType

# sale = Sale.objects.first()
# movement = Movement.objects.create(
#     content_type=ContentType.objects.get_for_model(Sale),
#     object_id=sale.id,
#     quantity=-5
# )

# print(movement.content_object)