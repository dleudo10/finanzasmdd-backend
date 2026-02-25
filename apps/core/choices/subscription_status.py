from django.db import models

class SubscriptionStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    ACTIVE = 'active', 'Activa'
    SUSPENDED = 'suspended', 'Suspendida'
    CANCELLED = 'cancelled', 'Cancelada'
    EXPIRED = 'expired', 'Expirada'