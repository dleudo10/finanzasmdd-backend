from django.db import models

class TimesTampTime(models.Model):
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de edición', auto_now=True)

    class Meta:
        abstract = True