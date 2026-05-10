from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'category', 'estimated_cost', 'duration_hours', 'is_popular']
    list_filter = ['category', 'city', 'is_popular']
    search_fields = ['name', 'description']
    list_editable = ['estimated_cost', 'is_popular']
