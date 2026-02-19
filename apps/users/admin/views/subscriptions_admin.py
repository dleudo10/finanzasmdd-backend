from django.contrib import admin, messages
from ...models import Subscription
from simple_history.admin import SimpleHistoryAdmin
from apps.core.choices import SubscriptionStatus
from datetime import timedelta
from django.db import transaction


@admin.register(Subscription)
class SubscriptionAdmin(SimpleHistoryAdmin):
    list_display = ('tenant', 'plan', 'status', 'start_date', 'end_date', 'observations')
    list_filter = ('tenant', 'plan', 'status', 'start_date', 'end_date',)
    search_fields = ('tenant', )
    ordering = ('-start_date',)
    actions = ['active_subscription']
    
    @admin.action(description='Activar suscripción')
    def active_subscription(modeladmin, request, queryset):
        pending = queryset.filter(status=SubscriptionStatus.PENDING).select_for_update()
        count = 0
            
        try:
            with transaction.atomic():
                for item in pending:
                    item.status = SubscriptionStatus.ACTIVE
                    item.end_date = item.start_date + timedelta(days=30)
                    item.save()
                    count += 1
                    
            modeladmin.message_user(
                request, 
                f"Éxito: {count} suscripción procesadas correctamente.",
                messages.SUCCESS
            )

        except Exception as e:
            modeladmin.message_user(
                request, 
                f"Error crítico: La operación fue cancelada para proteger los datos. Motivo: {e}",
                messages.ERROR
            )

    
    def get_actions(self, request):
        actions = super().get_actions(request)
        status_filter = request.GET.get('status__exact')
        
        # Solo eliminar si el filtro existe Y no es PENDING
        if status_filter and status_filter != str(SubscriptionStatus.PENDING):
            if 'active_subscription' in actions:
                del actions['active_subscription']
        return actions
    