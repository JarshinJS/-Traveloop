from django.contrib import admin
from .models import BudgetEntry


@admin.register(BudgetEntry)
class BudgetEntryAdmin(admin.ModelAdmin):
    list_display = ('trip', 'stop', 'category', 'description', 'amount', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('trip__name', 'description')
