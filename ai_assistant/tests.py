import json
from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from activities.models import Activity
from cities.models import City
from trips.models import Trip, TripActivity, TripStop


class ChatApiTests(TestCase):
    def test_chat_api_requires_post(self):
        response = self.client.get(reverse('ai_assistant:chat'))

        self.assertEqual(response.status_code, 405)

    def test_chat_api_uses_csrf_protection(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            reverse('ai_assistant:chat'),
            data=json.dumps({'message': 'dashboard'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 403)

    @override_settings(GEMINI_API_KEY='')
    def test_chat_api_returns_rule_based_fallback(self):
        response = self.client.post(
            reverse('ai_assistant:chat'),
            data=json.dumps({'message': 'dashboard'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard', response.json()['reply'])
        self.assertIn('links', response.json())


class SmartSuggestionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='traveler', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.city = City.objects.create(
            name='Rome',
            country='Italy',
            region='Europe',
            cost_index='100.00',
            popularity_score=90,
        )
        self.trip = Trip.objects.create(
            user=self.user,
            name='Europe',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 2),
            total_budget='100.00',
        )
        self.stop = TripStop.objects.create(
            trip=self.trip,
            city=self.city,
            arrival_date=date(2026, 6, 1),
            departure_date=date(2026, 6, 2),
        )
        used = Activity.objects.create(
            city=self.city,
            name='Food Tour',
            category='food',
            estimated_cost='20.00',
            duration_hours='2.0',
        )
        TripActivity.objects.create(stop=self.stop, activity=used)
        Activity.objects.create(
            city=self.city,
            name='Museum',
            category='culture',
            estimated_cost='40.00',
            duration_hours='2.0',
            is_popular=True,
        )
        Activity.objects.create(
            city=self.city,
            name='Luxury Transfer',
            category='transport',
            estimated_cost='500.00',
            duration_hours='1.0',
        )

    @override_settings(GEMINI_API_KEY='')
    def test_suggestions_are_budget_aware_and_diverse(self):
        self.client.login(username='traveler', password='pass12345')

        response = self.client.get(reverse('ai_assistant:suggestions', args=[self.trip.pk]))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        activity_names = [activity['name'] for activity in payload['activities']]
        self.assertIn('Museum', activity_names)
        self.assertNotIn('Food Tour', activity_names)
        self.assertNotIn('Luxury Transfer', activity_names)
        self.assertTrue(payload['ai_tip'])

    def test_suggestions_return_403_for_non_owner(self):
        self.client.login(username='other', password='pass12345')

        response = self.client.get(reverse('ai_assistant:suggestions', args=[self.trip.pk]))

        self.assertEqual(response.status_code, 403)
