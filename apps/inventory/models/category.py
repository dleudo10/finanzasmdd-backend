from django.db import models
from apps.core.models import (
    BaseState,
    TimesTampTime
)
from simple_history.models import HistoricalRecords
from apps.users.models import Tenant
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
 
class Category(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    name = models.CharField(
        'nombre', 
        max_length=150,
        validators=[MinLengthValidator(3, "Debe tener al menos 3 caracteres.")]
    )
    description = models.TextField(
        'descripción', 
        null=True, 
        blank=True,
        validators=[MinLengthValidator(10, "Debe tener al menos 10 caracteres.")]
    )
    history = HistoricalRecords()
    
    def delete(self, using=None, keep_parents=False):
        if self.products.filter(is_active=True).exists():
            raise ValidationError(f"No se puede eliminar la categoria {self.name} porque tiene productos activos")
        super().delete(using=using, keep_parents=keep_parents)
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower()
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tenant} - {self.name}"
    
    class Meta:
        db_table = "categories"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        constraints = [
            models.UniqueConstraint( 
                fields=["tenant", "name"],
                name="unique_category_name_tenant"
            )
        ]
        indexes = [
            models.Index(
                fields=["tenant", "created_at"], 
                name="idx_category_tenant_created_at"
            ),
        ]