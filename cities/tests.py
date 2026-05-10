from datetime import date
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from trips.models import Trip, TripStop
from .models import City


class CityViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='traveler', password='pass12345')
        self.paris = City.objects.create(
            name='Paris',
            country='France',
            region='Europe',
            cost_index='180.00',
            popularity_score=90,
        )
        self.tokyo = City.objects.create(
            name='Tokyo',
            country='Japan',
            region='Asia',
            cost_index='160.00',
            popularity_score=95,
        )

    def test_cities_root_uses_search_view(self):
        response = self.client.get('/cities/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Paris')

    def test_city_search_filters_with_q_object(self):
        response = self.client.get(reverse('city_search'), {'q': 'france'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Paris')
        self.assertNotContains(response, 'Tokyo')

    def test_add_to_trip_creates_stop_for_owner(self):
        trip = Trip.objects.create(
            user=self.user,
            name='Europe',
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 8),
        )
        self.client.login(username='traveler', password='pass12345')

        response = self.client.post(reverse('add_to_trip', args=[self.paris.pk]), {
            'trip_id': trip.pk,
        })

        self.assertRedirects(response, reverse('itinerary_builder', args=[trip.pk]))
        stop = TripStop.objects.get(trip=trip, city=self.paris)
        self.assertEqual(stop.arrival_date, trip.start_date)
        self.assertEqual(stop.departure_date, trip.start_date)

    def test_add_to_trip_rejects_other_users_trip(self):
        other = User.objects.create_user(username='other', password='pass12345')
        trip = Trip.objects.create(
            user=other,
            name='Private',
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 8),
        )
        self.client.login(username='traveler', password='pass12345')

        response = self.client.post(reverse('add_to_trip', args=[self.paris.pk]), {
            'trip_id': trip.pk,
        })

        self.assertEqual(response.status_code, 404)
        self.assertFalse(TripStop.objects.exists())


class SeedCitiesCommandTests(TestCase):
    def test_seed_cities_is_idempotent(self):
        out = StringIO()

        call_command('seed_cities', stdout=out)
        first_count = City.objects.count()
        call_command('seed_cities', stdout=out)

        self.assertEqual(first_count, 30)
        self.assertEqual(City.objects.count(), first_count)
        self.assertTrue(City.objects.filter(name='Paris', popularity_rating__gt=0).exists())
