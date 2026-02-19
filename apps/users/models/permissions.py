from django.db import models
from simple_history.models import HistoricalRecords

# === PERMISOS ===    
class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.code
    
    history = HistoricalRecords()
    
    class Meta:
        db_table = "permissions"
        verbose_name = "permiso"
        verbose_name_plural = "permisos"