from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from budget.models import BudgetEntry
from cities.models import City
from .forms import TripForm
from .models import PackingItem, Trip, TripNote, TripStop


class TripFormTests(TestCase):
    def test_end_date_cannot_be_before_start_date(self):
        form = TripForm(data={
            'name': 'Backwards Trip',
            'description': '',
            'start_date': '2026-06-10',
            'end_date': '2026-06-09',
            'total_budget': '1000.00',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Start date must be before or equal to the end date.', form.non_field_errors())

    def test_same_day_trip_is_valid(self):
        form = TripForm(data={
            'name': 'Day Trip',
            'description': '',
            'start_date': '2026-06-10',
            'end_date': '2026-06-10',
            'total_budget': '1000.00',
        })

        self.assertTrue(form.is_valid())


class TripModelStringTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='traveler', password='pass')
        self.trip = Trip.objects.create(
            user=self.user,
            name='Summer Loop',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
        )

    def test_packing_item_string_uses_name(self):
        item = PackingItem.objects.create(trip=self.trip, name='Passport')

        self.assertEqual(str(item), 'Passport')

    def test_trip_note_string_uses_title(self):
        note = TripNote.objects.create(trip=self.trip, title='Dinner ideas', content='Try the market.')

        self.assertEqual(str(note), 'Dinner ideas')


class TripRoutingAndViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='traveler', password='pass12345')
        self.city = City.objects.create(name='Rome', country='Italy', cost_index='140.00')
        self.trip = Trip.objects.create(
            user=self.user,
            name='Rome Loop',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5),
            total_budget='500.00',
            is_public=True,
        )

    def test_required_trip_urls_resolve(self):
        route_names = [
            ('trip_list', []),
            ('trip_create', []),
            ('trip_detail', [self.trip.pk]),
            ('trip_edit', [self.trip.pk]),
            ('trip_delete', [self.trip.pk]),
            ('reorder_stops', [self.trip.pk]),
            ('add_stop', [self.trip.pk]),
            ('trip_budget', [self.trip.pk]),
            ('packing_checklist', [self.trip.pk]),
            ('reset_packing', [self.trip.pk]),
            ('trip_notes', [self.trip.pk]),
            ('public_itinerary', [self.trip.share_token]),
            ('copy_trip', [self.trip.share_token]),
        ]

        for name, args in route_names:
            with self.subTest(name=name):
                self.assertIsNotNone(resolve(reverse(name, args=args)))
                self.assertIsNotNone(resolve(reverse(f'trips:{name}', args=args)))

    def test_trip_delete_is_post_only(self):
        self.client.login(username='traveler', password='pass12345')

        response = self.client.get(reverse('trip_delete', args=[self.trip.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Trip.objects.filter(pk=self.trip.pk).exists())

    def test_reorder_accepts_list_of_ids(self):
        stop_one = TripStop.objects.create(
            trip=self.trip,
            city=self.city,
            arrival_date=date(2026, 6, 1),
            departure_date=date(2026, 6, 2),
            order=0,
        )
        stop_two = TripStop.objects.create(
            trip=self.trip,
            city=self.city,
            arrival_date=date(2026, 6, 3),
            departure_date=date(2026, 6, 4),
            order=1,
        )
        self.client.login(username='traveler', password='pass12345')

        response = self.client.post(
            reverse('reorder_stops', args=[self.trip.pk]),
            data={'order': [stop_two.pk, stop_one.pk]},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        stop_one.refresh_from_db()
        stop_two.refresh_from_db()
        self.assertEqual(stop_two.order, 0)
        self.assertEqual(stop_one.order, 1)

    def test_clone_deep_copies_budget_packing_and_notes(self):
        stop = TripStop.objects.create(
            trip=self.trip,
            city=self.city,
            arrival_date=date(2026, 6, 1),
            departure_date=date(2026, 6, 2),
        )
        PackingItem.objects.create(trip=self.trip, name='Passport')
        TripNote.objects.create(trip=self.trip, stop=stop, title='Idea', content='Visit early.')
        BudgetEntry.objects.create(trip=self.trip, stop=stop, category='food', amount='40.00')
        clone_user = User.objects.create_user(username='clone', password='pass12345')
        self.client.login(username='clone', password='pass12345')

        response = self.client.post(reverse('copy_trip', args=[self.trip.share_token]))

        self.assertEqual(response.status_code, 302)
        copied = Trip.objects.get(user=clone_user)
        self.assertEqual(copied.stops.count(), 1)
        self.assertEqual(copied.packing_items.count(), 1)
        self.assertEqual(copied.notes.count(), 1)
        self.assertEqual(copied.budget_entries.count(), 1)
