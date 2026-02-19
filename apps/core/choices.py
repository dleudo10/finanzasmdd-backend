from django.db import models

# === Tipo de Persona ===
class TypePerson(models.TextChoices):
    NATURAL = 'N', 'Natural'
    LEGAL = 'J', 'Jurídica'
    
# === Tipo de Documeto ===
class TypeDocument(models.TextChoices):
    """Códigos definidos por la DIAN (Dirección de Impuestos y Aduanas Nacionales)"""
    
    CC = '13', 'Cédula de Ciudadanía'
    TE = '21', 'Tarjeta de Extranjería'
    CE = '22', 'Cédula de Extranjería'
    NIT = '31', 'NIT'
    PASSPORT = '41', 'Pasaporte'
    DE = '42', 'Documento Extranjero'
    
# === Estado de Suscripciones ===
class SubscriptionStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    ACTIVE = 'active', 'Activa'
    SUSPENDED = 'suspended', 'Suspendida'
    CANCELLED = 'cancelled', 'Cancelada'
    EXPIRED = 'expired', 'Expirada'

# PermissionList = [
#     {'code': 'users.create', 'description': ''},
#     {'code': 'users.read', 'description': ''},
#     {'code': 'users.update', 'description': ''},
#     {'code': 'users.delete', 'description': ''},
    
#     {'code': 'roles.create', 'description': ''},
#     {'code': 'roles.read', 'description': ''},
#     {'code': 'roles.update', 'description': ''},
#     {'code': 'roles.delete', 'description': ''},
# ]

