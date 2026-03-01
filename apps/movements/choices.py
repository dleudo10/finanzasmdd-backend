from django.db import models

class TypeMovementsChoices(models.TextChoices):
    PURCHASE = "PURCHASE", "COMPRA"
    SALE = "SALE", "VENTA"
    ADJUSTMENT = "ADJUSTMENT", "AJUSTE"
    INITIAL = "INITIAL", "INICIAL"