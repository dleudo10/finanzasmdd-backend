from django.db import models

class TypePriceChoices(models.TextChoices):
    SALE = "SALE", "Venta"
    PURCHASE = "PURCHASE", "compra"