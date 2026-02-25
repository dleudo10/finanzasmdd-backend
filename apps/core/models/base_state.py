from django.db import models

class BaseState(models.Model):
    is_active = models.BooleanField('estado activo', default=True)
    
    def change_status(self):
        """Alterna entre activo e inactivo"""
        self.is_active = not self.is_active
        self.save(update_fields=["is_active"])
    
    class Meta:
        abstract = True