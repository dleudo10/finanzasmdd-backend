from django.db import models

class TypePerson(models.TextChoices):
    NATURAL = 'N', 'Natural'
    LEGAL = 'J', 'Jurídica'