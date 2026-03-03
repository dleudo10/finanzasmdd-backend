from django.db import models

class BaseState(models.Model):
    is_active = models.BooleanField('estado', default=True)
    
    def change_status(self):
        self.is_active = not self.is_active
        self.save(update_fields=["is_active"])
        
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(update_fields=["is_active"])
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["is_active"]),
        ]