from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from trips.models import Trip, TripStop
from .models import BudgetEntry


class BudgetEntryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='traveler', password='pass12345')
        self.city = City.objects.create(name='Paris', country='France', cost_index='180.00')
        self.trip = Trip.objects.create(
            user=self.user,
            name='Paris Week',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 3),
            total_budget='100.00',
        )
        self.stop = TripStop.objects.create(
            trip=self.trip,
            city=self.city,
            arrival_date=date(2026, 6, 1),
            departure_date=date(2026, 6, 2),
        )

    def test_budget_entry_string(self):
        entry = BudgetEntry.objects.create(
            trip=self.trip,
            stop=self.stop,
            category='food',
            description='Dinner',
            amount='45.00',
        )

        self.assertEqual(str(entry), 'Dinner - Paris Week')

    def test_budget_page_creates_entry_for_trip(self):
        self.client.login(username='traveler', password='pass12345')

        response = self.client.post(reverse('trip_budget', args=[self.trip.pk]), {
            'stop': self.stop.pk,
            'category': 'activities',
            'description': 'Museum',
            'amount': '125.00',
        })

        self.assertRedirects(response, reverse('trip_budget', args=[self.trip.pk]))
        entry = BudgetEntry.objects.get(trip=self.trip)
        self.assertEqual(entry.stop, self.stop)
        self.assertEqual(entry.description, 'Museum')

    def test_budget_context_uses_entries_and_flags_over_budget(self):
        entry = BudgetEntry.objects.create(
            trip=self.trip,
            stop=self.stop,
            category='activities',
            amount='125.00',
        )
        entry.refresh_from_db()
        self.client.login(username='traveler', password='pass12345')

        response = self.client.get(reverse('trip_budget', args=[self.trip.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_estimated'], entry.amount)
        self.assertTrue(response.context['over_budget'])
        self.assertEqual(response.context['progress_percent'], 100)
