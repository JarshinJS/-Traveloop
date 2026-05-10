from django.urls import path
from .views import analytics_dashboard_view

app_name = 'admin_dashboard'

urlpatterns = [
    path('', analytics_dashboard_view, name='admin_analytics'),
]
