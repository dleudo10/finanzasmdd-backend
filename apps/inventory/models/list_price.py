from django.db import models
from apps.users.models import Tenant
from apps.core.models import BaseState, TimesTampTime
from simple_history.models import HistoricalRecords

class ListPrice(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    is_base = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(is_base=True),
                name="unique_active_list_price_per_tenant"
            )
        ]