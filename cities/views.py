from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import City
from trips.forms import TripStopForm
from trips.models import Trip


def city_search_view(request):
    cities = City.objects.all()
    query = request.GET.get('q', '')
    region = request.GET.get('region', '')

    if query:
        cities = cities.filter(
            models.Q(name__icontains=query) |
            models.Q(country__icontains=query) |
            models.Q(region__icontains=query)
        )

    if region:
        cities = cities.filter(region__iexact=region)

    regions = City.objects.values_list('region', flat=True).distinct().order_by('region')
    regions = [r for r in regions if r]  # filter out blanks

    context = {
        'cities': cities,
        'query': query,
        'selected_region': region,
        'regions': regions,
    }
    return render(request, 'cities/search.html', context)


def city_detail_view(request, pk):
    city = get_object_or_404(City, pk=pk)
    activities = city.activities.all()

    context = {
        'city': city,
        'activities': activities,
    }
    return render(request, 'cities/city_detail.html', context)


@login_required
@require_POST
def add_to_trip_view(request, pk):
    city = get_object_or_404(City, pk=pk)
    trip_id = request.POST.get('trip_id')

    if not trip_id:
        return _add_to_trip_error(request, 'Please select a trip.')

    if not str(trip_id).isdigit():
        return _add_to_trip_error(request, 'Please select a valid trip.')

    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    data = request.POST.copy()
    data['city'] = city.pk
    data.setdefault('arrival_date', trip.start_date)
    data.setdefault('departure_date', trip.start_date)

    form = TripStopForm(data)
    if not form.is_valid():
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        messages.error(request, 'Please fix the stop details and try again.')
        return redirect('city_detail', pk=city.pk)

    stop = form.save(commit=False)
    stop.trip = trip
    stop.city = city
    stop.order = trip.stops.count()
    stop.save()

    if _wants_json(request):
        return JsonResponse({
            'status': 'ok',
            'stop_id': stop.pk,
            'trip_id': trip.pk,
            'city_name': city.name,
            'arrival_date': stop.arrival_date.isoformat(),
            'departure_date': stop.departure_date.isoformat(),
        })

    messages.success(request, f'{city.name} was added to {trip.name}.')
    return redirect('itinerary_builder', pk=trip.pk)


def _add_to_trip_error(request, message):
    if _wants_json(request):
        return JsonResponse({'status': 'error', 'message': message}, status=400)
    messages.error(request, message)
    return redirect('city_search')


def _wants_json(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'
