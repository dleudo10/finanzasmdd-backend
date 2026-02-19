from django.db import models
from apps.core.models import (
    TimesTampTime,
    BaseState
)
from simple_history.models import HistoricalRecords
from .tenants import Tenant
from .permissions import Permission

# === ROLES ===
class Role(BaseState, TimesTampTime):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    is_owner_role = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.is_owner_role:
            raise models.ProtectedError(f"El rol {self.name} no puede eliminarse", self)
        return super().delete(*args, **kwargs)
    
    class Meta:
        db_table = 'roles'
        verbose_name = "rol"
        verbose_name_plural = "roles"
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'name'],
                name='roles_tenant_name_uk'
            ),
            models.UniqueConstraint(
                fields=['tenant'],
                condition=models.Q(is_owner_role=True),
                name='unique_owner_role_per_tenant'
            )
        ]