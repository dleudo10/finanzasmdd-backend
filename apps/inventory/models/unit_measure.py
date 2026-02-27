from django.db import models
from apps.core.models import TimesTampTime

class UnitMeasure(TimesTampTime):
    name = models.CharField(max_length=150, unique=True)  
    abbreviation = models.CharField(max_length=3, unique=True)
    
    def __str__(self):
        return f"{self.name} - ({self.abbreviation})"
    
    class Meta:
        db_table = "unit_measure"
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"