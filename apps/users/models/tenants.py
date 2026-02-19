from django.db import models
from django.utils.text import slugify
from apps.core.models import (
    TimesTampTime,
    BaseState
)
from apps.core.choices import (
    TypePerson,
    TypeDocument,
)
from django.contrib.auth import get_user_model
User = get_user_model()
from simple_history.models import HistoricalRecords


# === EMPRESA O COMPAÑIA ===
class Tenant(BaseState, TimesTampTime):
    owner = models.ForeignKey(
        User,
        verbose_name="Dueño",
        on_delete=models.PROTECT,
        related_name="owned_tenants"
    )
    trade_name = models.CharField('nombre comercial', max_length=200)
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True
    )
    type_person = models.CharField('tipo de persona', max_length=1, choices=TypePerson.choices, default=TypePerson.LEGAL)
    document_type = models.CharField('tipo de documento', max_length=2, choices=TypeDocument.choices, default=TypeDocument.NIT)
    document_number = models.CharField('numero de documento', max_length=15, unique=True)
    phone = models.CharField('telefono', max_length=10)
    adress = models.TextField('dirección', null=True, blank=True)
    
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
        
    def generate_unique_slug(self):
        base_slug = slugify(self.trade_name)
        slug = base_slug
        counter = 1
        
        while Tenant.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug
    
    def __str__(self):
        return self.trade_name

    class Meta:
        db_table = 'tenants'
        verbose_name = "compañia"
        verbose_name_plural = "compañias"
   