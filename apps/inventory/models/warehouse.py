from django.db import models
from apps.core.models import TimesTampTime, BaseState
from simple_history.models import HistoricalRecords
from apps.users.models import Tenant
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Warehouse(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    name = models.CharField(
        'nombre', 
        validators=[MinLengthValidator(3, "Debe tener al menos 3 caracteres.")],
        max_length=150
    )    
    location = models.CharField(
        'ubicación', 
        validators=[MinLengthValidator(3, "Debe tener al menos 3 caracteres.")],
        max_length=255, 
        null=True, 
        blank=True
    )
    observations = models.TextField(
        'observaciones', 
        validators=[MinLengthValidator(10, "Debe tener al menos 10 caracteres.")],
        null=True, 
        blank=True
    )
    is_default = models.BooleanField('por defecto', default=False)
    
    history = HistoricalRecords()
    
    def delete(self, using=None, keep_parents=False):
        if self.stocks.filter(quantity__gt=0).exists():
            raise ValidationError( f"No se puede eliminar la bodega '{self.name}' porque tiene stock disponible.")
        super().delete(using=using, keep_parents=keep_parents)
        
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "warehouse"
        verbose_name = "almacen"
        verbose_name_plural = "almacenes"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(is_default=True),
                name="unique_is_default_wh_per_tenant"
            ),
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_warehouse_name_tenant"
            )
        ]
        indexes = [
            models.Index(
                fields=["tenant", "created_at"], 
                name='idx_wh_tenant_created'
            ),
        ]
