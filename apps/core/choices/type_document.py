from django.db import models

class TypeDocument(models.TextChoices):
    """Códigos definidos por la DIAN (Dirección de Impuestos y Aduanas Nacionales)"""
    
    CC = '13', 'Cédula de Ciudadanía'
    TE = '21', 'Tarjeta de Extranjería'
    CE = '22', 'Cédula de Extranjería'
    NIT = '31', 'NIT'
    PASSPORT = '41', 'Pasaporte'
    DE = '42', 'Documento Extranjero'