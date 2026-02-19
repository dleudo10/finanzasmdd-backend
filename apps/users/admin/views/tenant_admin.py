from django.contrib import admin
from ...models import Tenant
from simple_history.admin import SimpleHistoryAdmin
from ..forms import TenantForm
from ...services.tenant.create_tenant import CreateTenantService

@admin.register(Tenant)
class TenantAdmin(SimpleHistoryAdmin):
    list_display = ('trade_name', 'type_person', 'document_type', 'document_number', 'phone', 'is_active', 'created_at')
    list_filter = ('trade_name', 'type_person', 'document_number', 'is_active',)
    search_fields = ('trade_name', 'document_number',)
    ordering = ('-created_at',)
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = TenantForm
        return super().get_form(request, obj, **kwargs)
        
    def save_model(self, request, obj, form, change):
        if not change:
            service_data = form.cleaned_data        
            service_data.pop("confirm_password", None) 
            CreateTenantService.execute(**service_data)
        else:
            super().save_model(request, obj, form, change)