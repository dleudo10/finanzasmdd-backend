from django.db import models
from apps.core.models import TimesTampTime, BaseState
from simple_history.models import HistoricalRecords
from apps.users.models import Tenant

class Warehouse(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField('nombre', max_length=150, unique=True)    
    location = models.CharField('ubicación', max_length=255, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    is_main = models.BooleanField('es principal', default=False)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "warehouse"
        verbose_name = "almacen"
        verbose_name_plural = "almacenes"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(is_main=True),
                name="unique_active_warehouse_per_tenant"
            )
        ]
