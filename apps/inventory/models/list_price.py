from django.db import models
from apps.users.models import Tenant
from apps.core.models import BaseState, TimesTampTime
from simple_history.models import HistoricalRecords

class ListPrice(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField('nombre', max_length=150, unique=True)
    is_main = models.BooleanField('es principal', default=False)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "list_price"
        verbose_name = "lista de precio"
        verbose_name_plural = "lista de precios"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(is_main=True),
                name="unique_active_list_price_per_tenant"
            )
        ]