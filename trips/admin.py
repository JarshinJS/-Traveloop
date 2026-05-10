from django.contrib import admin
from .models import Trip, TripStop, TripActivity, PackingItem, TripNote


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_public', 'created_at']
    list_filter = ['is_public', 'start_date']
    search_fields = ['name', 'user__username']
    readonly_fields = ['share_token', 'created_at', 'updated_at']


@admin.register(TripStop)
class TripStopAdmin(admin.ModelAdmin):
    list_display = ['trip', 'city', 'arrival_date', 'departure_date', 'order']
    list_filter = ['city']
    search_fields = ['trip__name', 'city__name']


@admin.register(TripActivity)
class TripActivityAdmin(admin.ModelAdmin):
    list_display = ['activity', 'stop', 'scheduled_date', 'scheduled_time']
    search_fields = ['activity__name']


@admin.register(PackingItem)
class PackingItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'category', 'is_packed']
    list_filter = ['category', 'is_packed']


@admin.register(TripNote)
class TripNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'trip', 'stop', 'created_at']
    search_fields = ['title', 'content']
