from django.db import models
from apps.core.models import TimesTampTime, BaseState
from simple_history.models import HistoricalRecords
from .unit_measure import UnitMeasure
from .product import Product
from apps.users.models import Tenant
from django.core.exceptions import ValidationError

class ProductUnit(BaseState, TimesTampTime):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="units_measure"
    )
    unit_measure = models.ForeignKey(
        UnitMeasure,
        on_delete=models.PROTECT
    )
    presentation_name = models.CharField('nombre de presentación', max_length=150)
    conversion_factor = models.DecimalField('factor de conversion', max_digits=12, decimal_places=6)
    is_base = models.BooleanField('medida base', default=False)
    sku = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.CharField(max_length=20, null=True, blank=True)
    plu = models.CharField(max_length=6, null=True, blank=True)
    requires_weight = models.BooleanField('requiere peso', default=False)
    
    history = HistoricalRecords()
    
    
    def clean(self):
        if self.conversion_factor <= 0:
            raise ValidationError({"conversion_factor": "El factor de conversión debe ser mayor que 0."})

        if self.is_base and self.conversion_factor != 1:
            raise ValidationError({"conversion_factor": "La unidad base debe tener un factor de conversión = 1."})
        
        if not self.is_base and (self.conversion_factor is None or self.conversion_factor <= 1):
            raise ValidationError({"conversion_factor": "El factor de conversión debe de ser mayor a 1"})
        
        if self.product.tenant_id != self.tenant_id:
            raise ValidationError({"product": "El producto no pertenece a la empresa"})    
        
        if not (self.sku or self.bar_code or self.plu):
            raise ValidationError("Debe ingresar al menos uno: SKU, Código de barras o PLU.")
        
        if  self.requires_weight and self.plu is None:
            raise ValidationError({"plu": "Es obligatorio"})
        
        if not self.is_base:
            base_exists = ProductUnit.objects.filter(
                product=self.product,
                tenant=self.tenant,
                is_base=True
            ).exclude(pk=self.pk).exists()

            if not base_exists:
                raise ValidationError(
                    "El producto debe tener al menos una unidad base."
                )
                
        if not self.pk:
            return 

        original = type(self).objects.get(pk=self.pk)

        has_movements = self.kardex.exists()

        if has_movements:
            restricted_fields = ["is_base", "sku", "bar_code", "plu"]

            for field in restricted_fields:
                if getattr(original, field) != getattr(self, field):
                    raise ValidationError({
                        field: "No se puede modificar este campo porque el producto ya tiene movimientos registrados."
                    })
            
    def delete(self, using=None, keep_parents=False):
        if self.is_base:
            raise ValidationError(
                f"No se puede eliminar la unidad base '{self.presentation_name}' del producto '{self.product}'."
            )
        return super().delete(using=using, keep_parents=keep_parents)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs) 
            
    def __str__(self):
        return f"{self.product} {self.unit_measure} - {self.conversion_factor}"
    
    class Meta:
        db_table = "products_unit"
        verbose_name = "Unidad de producto"
        verbose_name_plural = "Unidades de producto"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "product"],
                condition=models.Q(is_base=True),
                name="unique_base_unit_per_product_tenant"
            ),
            models.UniqueConstraint(
                fields=["tenant", "sku"],
                condition=models.Q(sku__isnull=False),
                name="unique_product_unit_sku_tenant"
            ),
            models.UniqueConstraint(
                fields=["tenant", "bar_code"],
                condition=models.Q(bar_code__isnull=False),
                name="unique_product_unit_bar_code_tenant"
            ),
            models.UniqueConstraint(
                fields=["tenant", "plu"],
                condition=models.Q(plu__isnull=False),
                name="unique_product_unit_plu_tenant"
            )
        ]