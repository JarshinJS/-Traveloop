"""
URL configuration for traveloop_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.urls import urlpatterns as account_patterns
from activities.urls import urlpatterns as activity_patterns
from admin_dashboard.urls import urlpatterns as admin_dashboard_patterns
from cities.urls import urlpatterns as city_patterns
from trips.urls import urlpatterns as trip_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(account_patterns)),
    path('accounts/', include((account_patterns, 'accounts'), namespace='accounts')),
    path('', include(trip_patterns)),
    path('', include((trip_patterns, 'trips'), namespace='trips')),
    path('cities/', include(city_patterns)),
    path('cities/', include((city_patterns, 'cities'), namespace='cities')),
    path('activities/', include(activity_patterns)),
    path('activities/', include((activity_patterns, 'activities'), namespace='activities')),
    path('admin-dashboard/', include(admin_dashboard_patterns)),
    path('admin-dashboard/', include((admin_dashboard_patterns, 'admin_dashboard'), namespace='admin_dashboard')),
    path('api/ai/', include('ai_assistant.urls', namespace='ai_assistant')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
