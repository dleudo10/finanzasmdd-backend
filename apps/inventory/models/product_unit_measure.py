from django.db import models
from apps.core.models import TimesTampTime
from simple_history.models import HistoricalRecords
from .unit_measure import UnitMeasure
from .product import Product
from apps.users.models import Tenant
from django.core.exceptions import ValidationError


class ProductUnitMeasure(TimesTampTime):
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
        
        if self.product.tenant_id != self.tenant_id:
            raise ValidationError({"product": "El producto no pertenece a la empresa"})    
        
        if not (self.sku or self.bar_code or self.plu):
            raise ValidationError("Debe ingresar al menos uno: SKU, Código de barras o PLU.")
    
    class Meta:
        db_table = "product_unit_measure"
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
        indexes = [
            models.Index(fields=["tenant", "product"]),
            models.Index(fields=["tenant", "sku"]),
            models.Index(fields=["tenant", "bar_code"]),
        ]