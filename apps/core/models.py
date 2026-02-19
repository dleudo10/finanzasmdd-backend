from django.db import models

# === MODELO DE ESTADO BASICO ===
class BaseState(models.Model):
    is_active = models.BooleanField('estado activo', default=True)
    
    def change_status(self):
        """Alterna entre activo e inactivo"""
        self.estado = not self.estado
        self.save(update_fields=["is_active"])
    
    class Meta:
        abstract = True
        
# === MARCA DE TIEMPO Y HORA ===
class TimesTampTime(models.Model):
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de edición', auto_now=True)

    class Meta:
        abstract = True