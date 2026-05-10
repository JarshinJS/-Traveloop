from django.contrib import admin
from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'region', 'cost_index', 'popularity_score']
    search_fields = ['name', 'country']
    list_filter = ['country', 'region']
    list_editable = ['cost_index', 'popularity_score']
