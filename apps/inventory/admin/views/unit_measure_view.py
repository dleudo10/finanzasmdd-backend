from django.contrib import admin
from ...models import UnitMeasure

@admin.register(UnitMeasure)
class UnitMeasureAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "created_at")
    search_fields = ("name", "abbreviation")
    ordering = ("-created_at",)