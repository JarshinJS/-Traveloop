import json
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

from trips.models import Trip
from cities.models import City
from activities.models import Activity


@staff_member_required
def analytics_dashboard_view(request):
    total_users = User.objects.count()
    total_trips = Trip.objects.count()
    public_trips = Trip.objects.filter(is_public=True).count()
    total_cities = City.objects.count()

    # Top cities by trip stops
    top_cities = City.objects.annotate(
        stop_count=Count('tripstop')
    ).order_by('-stop_count')[:10]

    # Top activities by usage
    top_activities = Activity.objects.annotate(
        usage_count=Count('tripactivity')
    ).order_by('-usage_count')[:10]

    # Trips per month (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    trips_per_month = (
        Trip.objects.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    month_labels = [t['month'].strftime('%b %Y') for t in trips_per_month]
    month_counts = [t['count'] for t in trips_per_month]

    # Recent users
    recent_users = User.objects.annotate(
        trip_count=Count('trips')
    ).order_by('-date_joined')[:10]

    # City chart data
    city_labels = [c.name for c in top_cities]
    city_counts = [c.stop_count for c in top_cities]

    context = {
        'total_users': total_users,
        'total_trips': total_trips,
        'public_trips': public_trips,
        'total_cities': total_cities,
        'top_cities': top_cities,
        'top_activities': top_activities,
        'recent_users': recent_users,
        'month_labels': json.dumps(month_labels),
        'month_counts': json.dumps(month_counts),
        'city_labels': json.dumps(city_labels),
        'city_counts': json.dumps(city_counts),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)
