import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

from .models import Trip, TripStop, TripActivity, PackingItem, TripNote
from .forms import TripForm, TripStopForm, PackingItemForm, TripNoteForm
from budget.forms import BudgetEntryForm
from cities.models import City
from activities.models import Activity


@login_required
def dashboard_view(request):
    user_trips = Trip.objects.filter(user=request.user).prefetch_related('stops__city')
    upcoming_trips = user_trips.filter(start_date__gte=timezone.now().date()).order_by('start_date')[:5]
    recent_trips = user_trips[:4]

    # Stats
    total_trips = user_trips.count()
    countries = set()
    for trip in user_trips.prefetch_related('stops__city'):
        for stop in trip.stops.all():
            if stop.city:
                countries.add(stop.city.country)

    # Countdown to next trip
    next_trip = upcoming_trips.first()
    countdown = None
    if next_trip:
        delta = next_trip.start_date - timezone.now().date()
        countdown = delta.days

    # Recommended cities
    recommended_cities = City.objects.order_by('-popularity_score')[:6]

    context = {
        'upcoming_trips': upcoming_trips,
        'recent_trips': recent_trips,
        'total_trips': total_trips,
        'countries_count': len(countries),
        'countdown': countdown,
        'next_trip': next_trip,
        'recommended_cities': recommended_cities,
    }
    return render(request, 'trips/dashboard.html', context)


@login_required
def trip_list_view(request):
    trips = Trip.objects.filter(user=request.user).prefetch_related('stops__city')
    query = request.GET.get('q', '')
    if query:
        trips = trips.filter(name__icontains=query)

    context = {
        'trips': trips,
        'query': query,
    }
    return render(request, 'trips/trip_list.html', context)


@login_required
def trip_create_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, f'Trip "{trip.name}" created successfully!')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm()

    return render(request, 'trips/create_trip.html', {'form': form})


@login_required
def trip_detail_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__city', 'stops__trip_activities__activity',
            'packing_items', 'notes__stop'
        ),
        pk=pk, user=request.user
    )

    stops = trip.stops.all()
    total_estimated = Decimal(str(trip.total_estimated_cost))
    over_budget = total_estimated > trip.total_budget if trip.total_budget > 0 else False

    # Packing stats
    packing_items = trip.packing_items.all()
    packed_count = packing_items.filter(is_packed=True).count()
    total_packing = packing_items.count()

    context = {
        'trip': trip,
        'stops': stops,
        'total_estimated': total_estimated,
        'over_budget': over_budget,
        'packing_items': packing_items,
        'packed_count': packed_count,
        'total_packing': total_packing,
        'notes': trip.notes.all(),
        'share_url': request.build_absolute_uri(f'/trips/share/{trip.share_token}/'),
    }
    return render(request, 'trips/trip_detail.html', context)


@login_required
def trip_edit_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated successfully!')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/create_trip.html', {'form': form, 'edit_mode': True, 'trip': trip})


@login_required
@require_POST
def trip_delete_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    name = trip.name
    trip.delete()
    messages.success(request, f'Trip "{name}" deleted.')
    return redirect('trip_list')


@login_required
def itinerary_builder_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__city', 'stops__trip_activities__activity'
        ),
        pk=pk, user=request.user
    )
    stop_form = TripStopForm()
    cities = City.objects.all().order_by('name')

    context = {
        'trip': trip,
        'stops': trip.stops.all(),
        'stop_form': stop_form,
        'cities': cities,
    }
    return render(request, 'trips/itinerary_builder.html', context)


@login_required
def itinerary_view_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__city', 'stops__trip_activities__activity'
        ),
        pk=pk, user=request.user
    )

    context = {
        'trip': trip,
        'stops': trip.stops.all(),
    }
    return render(request, 'trips/itinerary_view.html', context)


@login_required
@require_POST
def add_stop_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    form = TripStopForm(request.POST)
    if form.is_valid():
        stop = form.save(commit=False)
        stop.trip = trip
        stop.order = trip.stops.count()
        stop.save()
        return JsonResponse({
            'status': 'ok',
            'stop_id': stop.id,
            'city_name': stop.city.name if stop.city else '',
            'arrival_date': str(stop.arrival_date),
            'departure_date': str(stop.departure_date),
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_POST
def remove_stop_view(request, stop_id, pk=None):
    stop_query = TripStop.objects.filter(pk=stop_id, trip__user=request.user)
    if pk is not None:
        stop_query = stop_query.filter(trip_id=pk)
    stop = get_object_or_404(stop_query)
    stop.delete()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def add_activity_view(request, stop_id):
    stop = get_object_or_404(TripStop, pk=stop_id, trip__user=request.user)
    activity_id = request.POST.get('activity_id')
    if not activity_id:
        return JsonResponse({'status': 'error', 'message': 'Activity ID required'}, status=400)

    activity = get_object_or_404(Activity, pk=activity_id)
    ta, created = TripActivity.objects.get_or_create(
        stop=stop, activity=activity,
        defaults={
            'scheduled_date': stop.arrival_date,
        }
    )
    return JsonResponse({
        'status': 'ok',
        'created': created,
        'ta_id': ta.id,
        'activity_name': activity.name,
        'estimated_cost': float(activity.estimated_cost),
    })


@login_required
@require_POST
def remove_activity_view(request, ta_id):
    ta = get_object_or_404(TripActivity, pk=ta_id, stop__trip__user=request.user)
    ta.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def budget_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__city', 'budget_entries__stop__city'
        ),
        pk=pk, user=request.user
    )

    if request.method == 'POST':
        form = BudgetEntryForm(request.POST, trip=trip)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.trip = trip
            entry.save()
            messages.success(request, 'Budget entry added.')
            return redirect('trip_budget', pk=trip.pk)
        messages.error(request, 'Please fix the budget entry errors below.')
    else:
        form = BudgetEntryForm(trip=trip)

    entries = trip.budget_entries.select_related('stop__city')
    category_costs = {}
    city_costs = {}
    total_estimated = Decimal('0')

    for entry in entries:
        amount = entry.amount or Decimal('0')
        total_estimated += amount
        category = entry.get_category_display()
        category_costs[category] = category_costs.get(category, 0.0) + float(amount)
        city_name = entry.stop.city.name if entry.stop and entry.stop.city else 'General'
        city_costs[city_name] = city_costs.get(city_name, 0.0) + float(amount)

    stops_data = []
    for stop in trip.stops.all():
        stop_total = sum((entry.amount for entry in entries if entry.stop_id == stop.id), Decimal('0'))
        stops_data.append({
            'stop': stop,
            'activity_cost': stop_total,
            'stay_cost': Decimal('0'),
            'total': stop_total,
        })

    over_budget = total_estimated > trip.total_budget if trip.total_budget > 0 else False
    avg_per_day = total_estimated / trip.duration_days if trip.duration_days > 0 else Decimal('0')
    budget_utilization = (
        round((total_estimated / trip.total_budget) * 100, 2)
        if trip.total_budget > 0 else Decimal('0')
    )
    progress_percent = min(budget_utilization, Decimal('100'))

    context = {
        'trip': trip,
        'form': form,
        'entries': entries,
        'stops_data': stops_data,
        'total_estimated': total_estimated,
        'over_budget': over_budget,
        'avg_per_day': round(avg_per_day, 2),
        'budget_utilization': budget_utilization,
        'progress_percent': progress_percent,
        'category_costs': category_costs,
        'city_costs': city_costs,
        'budget_total': float(trip.total_budget),
    }
    return render(request, 'trips/budget.html', context)


@login_required
def packing_checklist_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)

    if request.method == 'POST':
        if 'reset' in request.POST:
            trip.packing_items.update(is_packed=False)
            messages.success(request, 'Checklist reset!')
            return redirect('packing_checklist', pk=pk)

        form = PackingItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.trip = trip
            item.save()
            messages.success(request, f'Added "{item.name}" to packing list.')
            return redirect('packing_checklist', pk=pk)
    else:
        form = PackingItemForm()

    items = trip.packing_items.all()
    packed_count = items.filter(is_packed=True).count()
    total_count = items.count()

    # Group by category
    categories = {}
    for item in items:
        cat = item.get_category_display()
        categories.setdefault(cat, []).append(item)

    context = {
        'trip': trip,
        'form': form,
        'categories': categories,
        'packed_count': packed_count,
        'total_count': total_count,
    }
    return render(request, 'trips/packing_checklist.html', context)


@login_required
@require_POST
def reset_packing_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    trip.packing_items.update(is_packed=False)
    messages.success(request, 'Checklist reset!')
    return redirect('packing_checklist', pk=pk)


@login_required
@require_POST
def toggle_packed_view(request, item_id):
    item = get_object_or_404(PackingItem, pk=item_id, trip__user=request.user)
    item.is_packed = not item.is_packed
    item.save()
    return JsonResponse({'status': 'ok', 'is_packed': item.is_packed})


@login_required
def notes_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related('notes__stop__city', 'stops__city'),
        pk=pk, user=request.user
    )

    if request.method == 'POST':
        form = TripNoteForm(request.POST, trip=trip)
        if form.is_valid():
            note = form.save(commit=False)
            note.trip = trip
            note.save()
            messages.success(request, 'Note added!')
            return redirect('trip_notes', pk=pk)
    else:
        form = TripNoteForm(trip=trip)

    context = {
        'trip': trip,
        'form': form,
        'notes': trip.notes.all(),
    }
    return render(request, 'trips/notes.html', context)


@login_required
def note_edit_view(request, note_id):
    note = get_object_or_404(TripNote, pk=note_id, trip__user=request.user)
    if request.method == 'POST':
        form = TripNoteForm(request.POST, instance=note, trip=note.trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated.')
            return redirect('trip_notes', pk=note.trip_id)
    else:
        form = TripNoteForm(instance=note, trip=note.trip)

    return render(request, 'trips/notes.html', {
        'trip': note.trip,
        'form': form,
        'notes': note.trip.notes.all(),
        'editing_note': note,
    })


@login_required
@require_POST
def note_delete_view(request, note_id):
    note = get_object_or_404(TripNote, pk=note_id, trip__user=request.user)
    note.delete()
    return JsonResponse({'status': 'ok'})


def public_itinerary_view(request, token):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__city', 'stops__trip_activities__activity'
        ),
        share_token=token, is_public=True
    )

    context = {
        'trip': trip,
        'stops': trip.stops.all(),
        'share_url': request.build_absolute_uri(),
    }
    return render(request, 'trips/public_itinerary.html', context)


@login_required
@require_POST
def copy_trip_view(request, token):
    original = get_object_or_404(
        Trip.objects.prefetch_related(
            'stops__trip_activities',
            'packing_items',
            'notes',
            'budget_entries',
        ),
        share_token=token,
        is_public=True,
    )

    new_trip = Trip.objects.create(
        user=request.user,
        name=f"Copy of {original.name}",
        description=original.description,
        start_date=original.start_date,
        end_date=original.end_date,
        total_budget=original.total_budget,
        is_public=False,
    )

    stop_map = {}
    for stop in original.stops.all():
        new_stop = TripStop.objects.create(
            trip=new_trip,
            city=stop.city,
            arrival_date=stop.arrival_date,
            departure_date=stop.departure_date,
            order=stop.order,
            notes=stop.notes,
        )
        stop_map[stop.id] = new_stop
        for ta in stop.trip_activities.all():
            TripActivity.objects.create(
                stop=new_stop,
                activity=ta.activity,
                scheduled_date=ta.scheduled_date,
                scheduled_time=ta.scheduled_time,
                notes=ta.notes,
            )

    for item in original.packing_items.all():
        PackingItem.objects.create(
            trip=new_trip,
            name=item.name,
            category=item.category,
        )

    for note in original.notes.all():
        TripNote.objects.create(
            trip=new_trip,
            stop=stop_map.get(note.stop_id),
            title=note.title,
            content=note.content,
        )

    for entry in original.budget_entries.all():
        new_trip.budget_entries.create(
            stop=stop_map.get(entry.stop_id),
            category=entry.category,
            description=entry.description,
            amount=entry.amount,
        )

    messages.success(request, f'Trip copied! You can now customize "{new_trip.name}".')
    return redirect('itinerary_builder', pk=new_trip.pk)


@login_required
@require_POST
def reorder_stops_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        order = data.get('order', [])
        if not isinstance(order, list):
            return JsonResponse({'status': 'error', 'message': 'Invalid order'}, status=400)

        if all(isinstance(stop_id, int) for stop_id in order):
            for position, stop_id in enumerate(order):
                TripStop.objects.filter(pk=stop_id, trip=trip).update(order=position)
        else:
            for item in order:
                TripStop.objects.filter(
                    pk=item['stop_id'], trip=trip
                ).update(order=item['order'])
        return JsonResponse({'status': 'ok'})
    except (json.JSONDecodeError, KeyError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
