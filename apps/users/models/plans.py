from django.db import models
from apps.core.models import (
    TimesTampTime,
    BaseState
)
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator


# === PLANES DE PAGO ===
class Plan(BaseState, TimesTampTime):
    name = models.CharField('nombre', max_length=200, unique=True)
    price = models.DecimalField('precio', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    user_limit = models.PositiveIntegerField('limite de usuarios')
    
    def __str__(self):
        return self.name
    
    history = HistoricalRecords()

    
    class Meta:
        db_table = "plans"
        verbose_name = "plan"
        verbose_name_plural = "planes"