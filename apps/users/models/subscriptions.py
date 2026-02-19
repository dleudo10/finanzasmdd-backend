from django.db import models
from simple_history.models import HistoricalRecords
from apps.core.choices import (
    SubscriptionStatus
)
from .tenants import Tenant
from .plans import Plan 
from django.core.exceptions import ValidationError

        
# === SUBSCRIPCIONES ===
class Subscription(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        verbose_name="compañia",
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )
    status = models.CharField('estado', max_length=10, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING)
    start_date = models.DateTimeField('fecha de inicio', auto_now_add=True)
    end_date = models.DateTimeField('fecha vigencia', null=True, blank=True)
    observations = models.TextField('observaciones', null=True, blank=True)
    
    history = HistoricalRecords()
    
    # Transiciones permitidas
    VALID_TRANSITIONS = {
        SubscriptionStatus.PENDING: [SubscriptionStatus.ACTIVE, SubscriptionStatus.CANCELLED],
        SubscriptionStatus.ACTIVE: [SubscriptionStatus.SUSPENDED, SubscriptionStatus.CANCELLED, SubscriptionStatus.EXPIRED],
        SubscriptionStatus.SUSPENDED: [SubscriptionStatus.ACTIVE, SubscriptionStatus.CANCELLED],
        SubscriptionStatus.EXPIRED: [], 
        SubscriptionStatus.CANCELLED: [],
    }
    
    def __str__(self):
        return f'{self.tenant.owner} - {self.plan} ({self.get_status_display()})'
    
    def clean(self):
        """Validación de lógica de negocio."""
        super().clean()
        if self.pk:
            old_status = Subscription.objects.get(pk=self.pk).status
            
            if old_status != self.status:
                allowed_next_statuses = self.VALID_TRANSITIONS.get(old_status, [])
                
                if self.status not in allowed_next_statuses:
                    raise ValidationError(
                        f"Transición no permitida: No se puede pasar de '{old_status}' a '{self.status}'."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = "suscripcion"
        verbose_name_plural = "suscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant"],
                condition=models.Q(status="active"),
                name="unique_active_subscription_per_tenant"
            )
        ]