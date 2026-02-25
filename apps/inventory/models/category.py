from django.db import models
from apps.core.models import (
    BaseState,
    TimesTampTime
)
from simple_history.models import HistoricalRecords
from apps.users.models import Tenant

class Category(BaseState, TimesTampTime):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    category = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    
    history = HistoricalRecords()
    
    
    def __str__(self):
        return super().__str__()