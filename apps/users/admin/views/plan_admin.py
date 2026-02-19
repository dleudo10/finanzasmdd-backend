from django.contrib import admin
from ...models import Plan
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Plan) 
class PlanAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'price', 'user_limit', 'is_active', 'created_at',)
    list_filter = ('name', 'price', 'is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    
    