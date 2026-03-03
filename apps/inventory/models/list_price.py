from django.db import models
from apps.users.models import Tenant
from apps.core.models import BaseState, TimesTampTime
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

class ListPrice(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    name = models.CharField('nombre', max_length=150)
    is_default = models.BooleanField('por defecto', default=False)
    
    history = HistoricalRecords()
    
    def delete(self, using=None, keep_parents=False):
        if self.is_default:
            raise ValidationError(f"No se puede eliminar la lista de precios '{self.name}' porque es la lista de precios por defecto")
        super().delete(using=using, keep_parents=keep_parents)
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "list_price"
        verbose_name = "lista de precio"
        verbose_name_plural = "lista de precios"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(is_default=True),
                name="unique_active_list_price_per_tenant"
            ),
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_list_price_name_tenant"
            )
        ]
        