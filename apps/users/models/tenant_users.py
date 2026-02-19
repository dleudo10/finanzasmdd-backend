from django.db import models
from apps.core.models import (
    TimesTampTime,
    BaseState 
)
from simple_history.models import HistoricalRecords
from .tenants import Tenant
from .roles import Role

from django.contrib.auth import get_user_model
User = get_user_model()
 
# === USUARIOS DENTRO DEL ESPACIO DEL SISTEMA ===  
class TenantUser(BaseState, TimesTampTime):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tenant_membership"
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="users"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="tenant_users"
    )
    
    history = HistoricalRecords()
    
    def __str__(self):
        return f'{self.user.name} {self.user.lastname}'
    
    class Meta:
        db_table = 'tenant_users'
        verbose_name = "tenant user"
        verbose_name_plural = "tenant users"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tenant"],
                name="unique_user_per_tenant"
            )
        ]
    