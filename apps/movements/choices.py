from django.db import models
    
class TypeMovementsChoices(models.TextChoices):
    INITIAL = "INITIAL", "Inventario Inicial"
    PURCHASE = "PURCHASE", "Compra"
    PURCHASE_RETURN = "PURCHASE_RETURN", "Devolución de Compra"
    SALE = "SALE", "Venta"
    SALE_RETURN = "SALE_RETURN", "Devolución de Venta"
    ADJUSTMENT_IN = "ADJUSTMENT_IN", "Ajuste de Entrada"
    ADJUSTMENT_OUT = "ADJUSTMENT_OUT", "Ajuste de Salida"
    TRANSFER_IN = "TRANSFER_IN", "Transferencia de Entrada"
    TRANSFER_OUT = "TRANSFER_OUT", "Transferencia de Salida"
    
class TypeNaturalityChoices(models.TextChoices):
    ENTRY = "ENTRY", "Entrada"
    EXIT = "EXIT", "Salida"